import os
import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Tuple

# Locate repo root and data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT_CACHE_FILE = os.path.join(BASE_DIR, "data", "open_mm_rl_cache.json")
HF_OPEN_MM_RL_URL = "https://datasets-server.huggingface.co/rows?dataset=TuringEnterprises%2FOpen-MM-RL&config=default&split=train"


class OpenMMRLService:
    """
    Production-grade service client for Hugging Face 'TuringEnterprises/Open-MM-RL' dataset API.
    Provides 2-tier resilience (live HF API with 15s timeout + local JSON disk cache fallback),
    along with heuristic STEM keyword classification mapping problems to APEX exam concept IDs.
    """

    # Keyword mappings to existing APEX Concept IDs
    CONCEPT_KEYWORDS = {
        "Physics": [
            ("phy_lorentz_force_circular_motion", "Lorentz Force & Magnetic Fields", [
                "magnetic", "lorentz", "solenoid", "magnetic field", "tesla", "ampere", "biot-savart", "flux", "galvanometer"
            ]),
            ("phy_coulomb_field", "Coulomb's Law & Electric Field", [
                "electric field", "coulomb", "charge", "electrostatic", "potential difference", "dipole", "permittivity"
            ]),
            ("phy_capacitance_circuits", "Capacitors & Dielectrics", [
                "capacitor", "capacitance", "dielectric", "rc circuit", "parallel plate"
            ]),
            ("phy_shm_oscillations", "Simple Harmonic Motion (SHM)", [
                "oscillation", "shm", "harmonic", "pendulum", "spring", "frequency", "damping", "amplitude", "resonance"
            ]),
            ("phy_work_energy_thm", "Work-Energy Theorem & Conservation", [
                "work-energy", "kinetic energy", "potential energy", "conservation of energy", "conservative force"
            ]),
            ("phy_newton_second_law", "Newton's Laws & Force Equilibrium", [
                "friction", "newton", "tension", "pulley", "free body", "equilibrium", "normal force", "acceleration"
            ]),
            ("phy_kinematics_1d_2d", "Kinematics & Projectile Motion", [
                "projectile", "trajectory", "velocity", "displacement", "parabolic motion", "relative velocity"
            ]),
            ("phy_carnot_efficiency", "Thermodynamics & Heat Cycles", [
                "thermodynamic", "carnot", "entropy", "adiabatic", "isothermal", "heat engine", "efficiency"
            ]),
            ("phy_refraction_tir", "Refraction, Optics & Total Internal Reflection", [
                "refraction", "optics", "snell", "focal length", "lens", "mirror", "total internal reflection", "prism"
            ]),
            ("phy_vectors_basic", "Vectors & Resolution of Forces", [
                "vector", "resultant", "magnitude", "cross product", "dot product", "orthogonal"
            ]),
        ],
        "Mathematics": [
            ("math_area_curves", "Area Under Curves & Definite Integration", [
                "area of the shaded region", "area enclosed", "bounded by the curve", "area between curves", "region enclosed"
            ]),
            ("math_definite_properties", "Definite Integrals & King's Rule", [
                "integral", "integration", "definite integral", "riemann", "leibniz", "indefinite integral", "antiderivative"
            ]),
            ("math_functions_domain_range", "Functions, Polynomials & Algebra", [
                "polynomial", "irreducible", "monic", "field theory", "finite field", "ideal class group", "degree of", "bijection", "domain and range"
            ]),
            ("math_scalar_triple_product", "Vectors & 3D Geometry", [
                "coplanar", "triple product", "plane", "direction cosines", "vector", "direction ratios", "3d coordinate"
            ]),
            ("math_quadratic_roots", "Roots & Quadratic Equations", [
                "quadratic", "discriminant", "roots of the equation", "real roots", "polynomial roots"
            ]),
            ("math_complex_modulus", "Complex Numbers & Modulus", [
                "complex number", "imaginary", "modulus", "argument", "de moivre", "roots of unity"
            ]),
            ("math_conditional_probability", "Probability & Discrete Mathematics", [
                "probability", "bayes", "graph theory", "dominating function", "vertices", "edges", "combinatorics", "permutation", "combination"
            ]),
            ("math_limits", "Limits & Continuity", [
                "limit", "continuity", "l'hopital", "indeterminate", "differentiability"
            ]),
        ],
        "Chemistry": [
            ("chem_chemical_equil_kp_kc", "Chemical Equilibrium (Kp & Kc)", [
                "equilibrium constant", "kp", "kc", "le chatelier", "reaction quotient", "dissociation constant"
            ]),
            ("chem_first_law_thermo", "Thermodynamics & Enthalpy", [
                "enthalpy", "calorimetry", "hess's law", "internal energy", "heat of formation", "heat of combustion"
            ]),
            ("chem_entropy_gibbs", "Entropy & Gibbs Free Energy", [
                "gibbs free energy", "entropy", "spontaneity", "delta g", "delta h", "delta s"
            ]),
            ("chem_kinetics_half_life_order", "Chemical Kinetics & Reaction Rates", [
                "rate law", "rate constant", "activation energy", "arrhenius", "half-life", "first-order", "second-order"
            ]),
            ("chem_ionic_ph_buffer", "Ionic Equilibrium & Buffers", [
                "buffer", "ph calculation", "pka", "pkb", "solubility product", "ksp", "henderson-hasselbalch"
            ]),
            ("chem_nernst_equation", "Electrochemistry & Nernst Equation", [
                "nernst", "galvanic cell", "cell potential", "electrochemical", "emf", "electrode potential", "faraday"
            ]),
            ("chem_hybridization_expanded_octet", "Chemical Bonding & Molecular Structure", [
                "hybridization", "molecular geometry", "vsepr", "bond order", "octet", "lewis structure", "dipole moment"
            ]),
            ("chem_electronic_effects", "Organic Mechanisms & Reaction Intermediates", [
                "nucleophilic", "electrophilic", "resonance", "carbocation", "isomerism", "sn1", "sn2", "hyperconjugation"
            ]),
        ],
        "Biology": [
            ("bio_prokaryote_vs_eukaryote", "Cellular Architecture & Prokaryotes", [
                "prokaryote", "eukaryote", "cell wall", "peptidoglycan", "ribosome", "plasma membrane", "gram-positive"
            ]),
            ("bio_cell_organelles", "Endomembrane System & Organelles", [
                "mitochondria", "chloroplast", "golgi apparatus", "endoplasmic reticulum", "lysosome", "vacuole", "nucleus"
            ]),
            ("bio_cell_cycle_mitosis_meiosis", "Cell Cycle, Mitosis & Meiosis", [
                "mitosis", "meiosis", "chromatid", "anaphase", "metaphase", "interphase", "telophase", "cytokinesis", "spindle"
            ]),
            ("bio_mendelian_laws", "Genetics & Mendelian Inheritance", [
                "mendel", "allele", "heterozygous", "homozygous", "genotype", "phenotype", "punnett", "monohybrid", "dihybrid"
            ]),
            ("bio_c4_pathway_hatch_slack", "Photosynthesis & Metabolic Pathways", [
                "photosynthesis", "calvin cycle", "c4 pathway", "krantz anatomy", "rubisco", "pep carboxylase", "chlorophyll"
            ]),
            ("bio_blood_cardiac_cycle", "Circulatory Physiology & Cardiac Cycle", [
                "cardiac cycle", "systole", "diastole", "ecg", "artery", "ventricle", "atrium", "hemoglobin", "blood group"
            ]),
            ("bio_nephron_countercurrent_mechanism", "Excretory System & Nephron Physiology", [
                "nephron", "glomerulus", "countercurrent", "bowman's capsule", "loop of henle", "renal", "osmoregulation"
            ]),
        ]
    }

    def __init__(self, cache_file: str = DEFAULT_CACHE_FILE):
        self.cache_file = cache_file
        self.cached_rows: List[Dict[str, Any]] = []
        self._load_cache()

    def _load_cache(self) -> None:
        """Loads cached rows from disk file for offline resilience."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.cached_rows = data.get("rows", [])
                    elif isinstance(data, list):
                        self.cached_rows = data
            except Exception as e:
                print(f"[OpenMMRLService] Warning loading cache from {self.cache_file}: {e}")
                self.cached_rows = []

    def _save_cache(self) -> None:
        """Saves current cache to disk file."""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump({"rows": self.cached_rows}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[OpenMMRLService] Warning saving cache to {self.cache_file}: {e}")

    def classify_stem_problem(
        self,
        question_text: str,
        domain: str = "",
        subdomain: str = ""
    ) -> Dict[str, str]:
        """
        Classifies a STEM problem by checking keywords across Physics, Mathematics,
        Chemistry, and Biology to map to existing APEX concept IDs.
        """
        combined = f"{domain} {subdomain} {question_text}".lower()

        # Score matches for each category and concept
        best_match = None
        highest_score = 0
        assigned_category = "Mathematics"  # Default fallback for Open-MM-RL

        # Priority 1: Check keyword presence across all disciplines
        for category, concept_list in self.CONCEPT_KEYWORDS.items():
            for concept_id, concept_name, keywords in concept_list:
                score = 0
                for kw in keywords:
                    if kw in combined:
                        # Longer keyword matches get higher weight
                        score += len(kw.split()) * 2
                if score > highest_score:
                    highest_score = score
                    assigned_category = category
                    best_match = {
                        "category": category,
                        "concept_id": concept_id,
                        "concept_name": concept_name,
                        "exam": "NEET" if category == "Biology" else "JEE"
                    }

        # If keywords scored a match, return it
        if best_match and highest_score > 0:
            return best_match

        # Priority 2: Fallback to domain/subdomain strings
        domain_lower = domain.lower()
        if "phys" in domain_lower:
            return {
                "category": "Physics",
                "concept_id": "phy_vectors_basic",
                "concept_name": "Vectors & Resolution of Forces",
                "exam": "JEE"
            }
        elif "chem" in domain_lower:
            return {
                "category": "Chemistry",
                "concept_id": "chem_first_law_thermo",
                "concept_name": "Thermodynamics & Enthalpy",
                "exam": "JEE"
            }
        elif "bio" in domain_lower or "life" in domain_lower:
            return {
                "category": "Biology",
                "concept_id": "bio_cell_organelles",
                "concept_name": "Endomembrane System & Organelles",
                "exam": "NEET"
            }

        # Default fallback for Open-MM-RL (majority Math/Physics)
        return {
            "category": "Mathematics",
            "concept_id": "math_functions_domain_range",
            "concept_name": "Functions, Polynomials & Algebra",
            "exam": "JEE"
        }

    def _normalize_row(self, raw_row: Dict[str, Any], row_idx: int = 0) -> Dict[str, Any]:
        """
        Structures raw dataset row into unified APEX problem model.
        Extracts question, answer, multimodal images, and maps to exam concept ID.
        """
        # Some HF responses nest inside "row"
        data = raw_row.get("row", raw_row)

        question = data.get("question", "")
        answer = str(data.get("answer", "")).strip()
        domain = data.get("domain", "Math")
        subdomain = data.get("subDomain", "")
        conv_id = str(data.get("conversation_id", f"open_mm_rl_{row_idx}"))

        # Multimodal image handling
        images = []
        raw_images = data.get("images", [])
        if isinstance(raw_images, list):
            for img in raw_images:
                if isinstance(img, dict) and "src" in img:
                    images.append({
                        "src": img["src"],
                        "width": img.get("width"),
                        "height": img.get("height")
                    })
                elif isinstance(img, str):
                    images.append({"src": img})

        classification = self.classify_stem_problem(question, domain=domain, subdomain=subdomain)

        # Generate 4 multiple-choice options for drill simulation
        clean_ans = re.sub(r"[\\\[\]\$\s]", "", answer)
        if not clean_ans:
            clean_ans = "Option A"
            
        options = [
            f"{answer}",
            f"{clean_ans} + \\sqrt{{2}}",
            f"\\frac{{{clean_ans}}}{{2}}",
            f"-{clean_ans}"
        ]

        return {
            "id": conv_id,
            "domain": domain,
            "subdomain": subdomain,
            "category": classification["category"],
            "subject": classification["category"],
            "concept_id": classification["concept_id"],
            "concept_name": classification["concept_name"],
            "exam": classification["exam"],
            "question": question,
            "answer": answer,
            "images": images,
            "has_multimodal": len(images) > 0,
            "options": options,
            "correct_option": 0,
            "difficulty": "Olympiad / RL-Trained",
            "source": "TuringEnterprises/Open-MM-RL"
        }

    def fetch_live_rows(
        self,
        offset: int = 0,
        length: int = 10,
        timeout: int = 15
    ) -> Dict[str, Any]:
        """
        Fetches live rows from the Hugging Face API with a 2-tier resilience pattern:
        Tier 1: Try HTTP GET to Hugging Face datasets-server API (15s timeout).
        Tier 2: If network call fails or times out, immediately fall back to local disk cache.
        """
        url = f"{HF_OPEN_MM_RL_URL}&offset={offset}&length={length}"
        source = "cache_fallback"
        raw_items: List[Dict[str, Any]] = []

        # Tier 1: Try live API
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "AdaptiveIntelligenceEngine/1.0 (STEM; Live Datasets Client)"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
                api_rows = payload.get("rows", [])
                if api_rows:
                    source = "live_hf_api"
                    raw_items = api_rows

                    # Merge new items into local cache to enrich future offline fallback
                    existing_ids = {
                        str(r.get("row", r).get("conversation_id"))
                        for r in self.cached_rows
                    }
                    for nr in api_rows:
                        cid = str(nr.get("row", nr).get("conversation_id"))
                        if cid and cid not in existing_ids:
                            self.cached_rows.append(nr)
                            existing_ids.add(cid)
                    self._save_cache()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception) as err:
            print(f"[OpenMMRLService] Notice: Live HF fetch failed/timed out ({err}). Using Tier 2 local cache.")
            source = "cache_fallback"

        # Tier 2: Local cache fallback
        if not raw_items:
            if not self.cached_rows:
                self._load_cache()
            raw_items = self.cached_rows[offset: offset + length]

        # Structure and classify each problem
        problems = [
            self._normalize_row(item, row_idx=offset + i)
            for i, item in enumerate(raw_items)
        ]

        return {
            "total": len(problems),
            "offset": offset,
            "length": length,
            "source": source,
            "problems": problems,
            # Also provide alias "rows" for compatibility with raw callers
            "rows": problems
        }
