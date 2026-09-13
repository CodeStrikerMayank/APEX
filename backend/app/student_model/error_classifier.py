from typing import Optional, Dict, Any

class ErrorClassifier:
    """
    Classifies student errors based on question distractors, response time anomalies, and attempt patterns.
    """
    @staticmethod
    def classify_error(
        question_distractor_explanations: Optional[Dict[str, str]],
        student_answer: Optional[str],
        correct_answer: str,
        time_taken_seconds: int,
        estimated_time_seconds: int = 60
    ) -> Dict[str, Any]:
        """
        Determines the most probable root cause error category.
        """
        if student_answer == correct_answer:
            return {"error_type": None, "note": "Correct response."}

        if not student_answer:
            return {
                "error_type": "TIME_PRESSURE" if time_taken_seconds >= estimated_time_seconds else "SKIPPED",
                "note": "Question was skipped or timed out without answer selection."
            }

        # Check if question distractor metadata contains an explicit tag
        if question_distractor_explanations and student_answer in question_distractor_explanations:
            raw_text = question_distractor_explanations[student_answer]
            for tag in [
                "CONCEPTUAL_ERROR", "FORMULA_SELECTION_ERROR", "CALCULATION_ERROR",
                "SIGN_ERROR", "UNIT_ERROR", "READING_ERROR", "CARELESS_ERROR"
            ]:
                if tag in raw_text:
                    return {
                        "error_type": tag,
                        "note": raw_text
                    }

        # Fast response with wrong answer -> likely careless or guess
        if time_taken_seconds < max(10, estimated_time_seconds * 0.20):
            return {
                "error_type": "GUESS",
                "note": f"Answer submitted very rapidly ({time_taken_seconds}s vs {estimated_time_seconds}s expected)."
            }

        # Prolonged response with wrong answer -> concept or calculation struggle
        if time_taken_seconds > estimated_time_seconds * 2.0:
            return {
                "error_type": "CONCEPTUAL_ERROR",
                "note": f"Significant deliberation time ({time_taken_seconds}s), indicating conceptual struggle."
            }

        return {
            "error_type": "UNKNOWN",
            "note": "Standard incorrect attempt."
        }


class CodeTraceDissector:
    """
    Structured AST and Error Trace Dissection Preprocessor:
    Deconstructs student code snippets, compiler outputs, and stack traces
    into deterministic structural diagnostics before passing to the LLM prompt.
    """
    import ast
    import re

    @classmethod
    def dissect_code(cls, code_str: str) -> Dict[str, Any]:
        """
        Parses code string via Python AST to detect syntax faults, recursion patterns,
        loop structures, and bracket matching.
        """
        import ast

        if not code_str or not code_str.strip():
            return {"is_code": False, "valid_syntax": True, "diagnostics": "Empty code snippet"}

        # First check delimiter balance
        delim_check = cls.check_delimiter_balance(code_str)
        if not delim_check["balanced"]:
            return {
                "is_code": True,
                "valid_syntax": False,
                "fault_category": "UNCLOSED_DELIMITER",
                "fault_message": delim_check["error"],
                "ast_metrics": None
            }

        try:
            tree = ast.parse(code_str)
            metrics = {
                "total_nodes": len(list(ast.walk(tree))),
                "functions": [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)],
                "has_loops": any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(tree)),
                "has_conditionals": any(isinstance(n, ast.If) for n in ast.walk(tree)),
                "has_recursion": False
            }

            # Check if any function calls itself
            for f in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
                calls = [n.func.id for n in ast.walk(f) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
                if f.name in calls:
                    metrics["has_recursion"] = True
                    break

            return {
                "is_code": True,
                "valid_syntax": True,
                "fault_category": None,
                "fault_message": "Syntactically sound AST",
                "ast_metrics": metrics
            }
        except SyntaxError as e:
            return {
                "is_code": True,
                "valid_syntax": False,
                "fault_category": "SYNTAX_ERROR",
                "fault_line": e.lineno,
                "fault_offset": e.offset,
                "fault_line_text": (e.text or "").strip(),
                "fault_message": e.msg,
                "ast_metrics": None
            }
        except Exception as ex:
            return {
                "is_code": True,
                "valid_syntax": False,
                "fault_category": "PARSE_EXCEPTION",
                "fault_message": str(ex),
                "ast_metrics": None
            }

    @classmethod
    def check_delimiter_balance(cls, code_str: str) -> Dict[str, Any]:
        """Validates matching parentheses, brackets, and curly braces."""
        pairs = {')': '(', ']': '[', '}': '{'}
        stack = []
        for idx, ch in enumerate(code_str):
            if ch in pairs.values():
                stack.append((ch, idx))
            elif ch in pairs.keys():
                if not stack or stack[-1][0] != pairs[ch]:
                    return {
                        "balanced": False,
                        "error": f"Mismatched closing delimiter '{ch}' at character position {idx}"
                    }
                stack.pop()

        if stack:
            unmatched = stack[-1]
            return {
                "balanced": False,
                "error": f"Unclosed opening delimiter '{unmatched[0]}' at character position {unmatched[1]}"
            }
        return {"balanced": True, "error": None}

    @classmethod
    def dissect_traceback(cls, trace_text: str) -> Dict[str, Any]:
        """
        Dissects runtime stack traces or compiler error outputs into structured fields:
        exception type, failing frame, failing line number, and root cause message.
        """
        import re

        if not trace_text or not trace_text.strip():
            return {"is_traceback": False}

        lines = [line.strip() for line in trace_text.strip().split("\n") if line.strip()]

        # Search for Exception: message on last lines
        exc_match = None
        for line in reversed(lines):
            m = re.search(r'\b([A-Za-z]+Error|[A-Za-z]+Exception):\s*(.*)', line)
            if m:
                exc_match = m
                break

        # Search for File "...", line X, in Y
        frame_matches = re.findall(r'File\s+["\'](.*?)["\'],\s+line\s+(\d+)(?:,\s+in\s+(\w+))?', trace_text)

        frames = []
        for fm in frame_matches:
            frames.append({
                "file": fm[0],
                "line": int(fm[1]),
                "scope": fm[2] if fm[2] else "<module>"
            })

        if exc_match or frames:
            return {
                "is_traceback": True,
                "exception_type": exc_match.group(1) if exc_match else "RUNTIME_FAULT",
                "exception_message": exc_match.group(2).strip() if exc_match else lines[-1],
                "failing_frame": frames[-1] if frames else None,
                "call_stack_depth": len(frames),
                "frames": frames
            }

        # Check for compiler style errors: file.cpp:line:col: error: msg
        compiler_match = re.search(r'([a-zA-Z0-9_\.\-]+):(\d+):(\d+):\s*(error|warning):\s*(.*)', trace_text, re.I)
        if compiler_match:
            return {
                "is_traceback": True,
                "exception_type": f"COMPILER_{compiler_match.group(4).upper()}",
                "exception_message": compiler_match.group(5).strip(),
                "failing_frame": {
                    "file": compiler_match.group(1),
                    "line": int(compiler_match.group(2)),
                    "column": int(compiler_match.group(3))
                },
                "call_stack_depth": 1,
                "frames": []
            }

        return {"is_traceback": False}

    @classmethod
    def preprocess_troubleshooting_input(cls, text: str) -> Dict[str, Any]:
        """
        Preprocesses arbitrary troubleshooting inputs (code, stack trace, or math snippet)
        and yields structured analytical context for the LLM.
        """
        tb = cls.dissect_traceback(text)
        if tb.get("is_traceback"):
            return {"type": "TRACEBACK", "dissection": tb}

        # Check if text looks like code (contains def, class, import, for, while, return, or brackets)
        code_markers = ["def ", "class ", "import ", "for ", "while ", "return ", "if ", "{", "}"]
        if any(marker in text for marker in code_markers) or "\n" in text:
            code_diag = cls.dissect_code(text)
            if code_diag.get("is_code"):
                return {"type": "CODE_SNIPPET", "dissection": code_diag}

        return {"type": "NATURAL_LANGUAGE", "dissection": None}

