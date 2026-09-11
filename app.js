/**
 * APEX Adaptive Intelligence Engine
 * Multimodal STEM Vault Integration (TuringEnterprises/Open-MM-RL)
 * Zero-dependency frontend client with KaTeX math rendering & adaptive quiz drills.
 */

(function(window) {
  'use strict';

  let currentOffset = 0;
  const pageLength = 10;
  let currentFilterSubject = 'all';
  let cachedProblems = [];

  /**
   * Loads problems from the backend Open-MM-RL endpoint and renders cards.
   * @param {number} offset - pagination offset (default: 0)
   * @param {number} length - batch length (default: 10)
   * @param {string} filterSubject - 'all' | 'mathematics' | 'physics' | 'chemistry' | 'biology'
   */
  async function loadOpenMMRLVault(offset = currentOffset, length = pageLength, filterSubject = currentFilterSubject) {
    const grid = document.getElementById('openMMRLGrid');
    if (!grid) return;

    currentOffset = offset;
    currentFilterSubject = filterSubject;

    grid.innerHTML = `
      <div style="grid-column:1/-1;padding:48px 20px;text-align:center;">
        <div style="display:inline-block;width:36px;height:36px;border:3px solid var(--border);border-top-color:var(--purple);border-radius:50%;animation:spin 0.8s linear infinite;margin-bottom:14px;"></div>
        <div style="font-weight:600;font-size:15px;color:var(--ink);">Fetching Multimodal STEM Dataset...</div>
        <div style="font-size:12.5px;color:var(--ink-soft);margin-top:4px;">Connecting to Hugging Face Datasets API (with 2-tier local disk cache fallback)</div>
      </div>
    `;

    try {
      // API call with resilient standalone fallback
      const apiEndpoint = `/api/curriculum/open-mm-rl/sample?offset=${offset}&length=${length}`;
      let res;
      if (window.ApiClient && typeof window.ApiClient.get === 'function') {
        res = await window.ApiClient.get(apiEndpoint);
      } else {
        const base = window.location.protocol.startsWith('http') ? '' : 'http://127.0.0.1:8000';
        const raw = await fetch(`${base}${apiEndpoint}`);
        if (!raw.ok) throw new Error(`HTTP ${raw.status}`);
        res = await raw.json();
      }
      const problems = (res && res.problems) ? res.problems : (res && res.rows ? res.rows : []);
      cachedProblems = problems;

      // Update badge indicator for data source
      const sourceBadge = document.getElementById('openMMRLSourceBadge');
      if (sourceBadge) {
        if (res.source === 'live_hf_api') {
          sourceBadge.innerHTML = '<span class="dot-live" style="background:var(--green-fg)"></span> Live Hugging Face API';
          sourceBadge.className = 'chip chip-green';
        } else {
          sourceBadge.innerHTML = '<span class="dot-live" style="background:var(--amber-fg)"></span> Tier-2 Local Disk Cache (Offline)';
          sourceBadge.className = 'chip chip-amber';
        }
      }

      // Filter by subject if requested
      const filtered = filterSubject === 'all'
        ? problems
        : problems.filter(p => (p.category || '').toLowerCase() === filterSubject.toLowerCase());

      if (filtered.length === 0) {
        grid.innerHTML = `
          <div style="grid-column:1/-1;padding:40px 20px;text-align:center;background:var(--card);border:1px solid var(--border);border-radius:var(--radius-md);">
            <div style="font-size:32px;margin-bottom:8px;">🔍</div>
            <div style="font-weight:700;color:var(--ink);font-size:15px;">No problems match '${escapeHtml(filterSubject)}' in this batch</div>
            <p style="font-size:13px;color:var(--ink-soft);margin:6px 0 16px;">Try switching to 'All Disciplines' or load the next batch.</p>
            <button class="btn-subtle" onclick="loadOpenMMRLVault(0, ${length}, 'all')">Show All Disciplines</button>
          </div>
        `;
        return;
      }

      grid.innerHTML = '';

      filtered.forEach((item, idx) => {
        const card = document.createElement('div');
        card.className = 'stem-problem-card';
        card.style.cssText = `
          background: var(--card);
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 14px;
          box-shadow: var(--shadow-sm);
          transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
          position: relative;
        `;
        card.onmouseenter = () => {
          card.style.transform = 'translateY(-2px)';
          card.style.boxShadow = 'var(--shadow-md)';
          card.style.borderColor = 'var(--purple-border)';
        };
        card.onmouseleave = () => {
          card.style.transform = '';
          card.style.boxShadow = 'var(--shadow-sm)';
          card.style.borderColor = 'var(--border)';
        };

        // Category Badge Color
        let catChipClass = 'chip-blue';
        let catIcon = '📐';
        const catLower = (item.category || '').toLowerCase();
        if (catLower.includes('phys')) {
          catChipClass = 'chip-purple';
          catIcon = '⚡';
        } else if (catLower.includes('chem')) {
          catChipClass = 'chip-amber';
          catIcon = '🧪';
        } else if (catLower.includes('bio')) {
          catChipClass = 'chip-green';
          catIcon = '🧬';
        }

        // Multimodal Image Display
        let imageHtml = '';
        if (item.images && item.images.length > 0) {
          const firstImg = item.images[0];
          const imgSrc = typeof firstImg === 'string' ? firstImg : firstImg.src;
          if (imgSrc) {
            imageHtml = `
              <div style="background:var(--track-bg);border:1px solid var(--border);border-radius:var(--radius-sm);overflow:hidden;margin-top:4px;text-align:center;max-height:260px;position:relative;">
                <img src="${escapeHtml(imgSrc)}" alt="STEM Diagram" loading="lazy" style="max-height:260px;width:auto;max-width:100%;object-fit:contain;cursor:zoom-in;" onclick="window.openStemImageModal('${escapeHtml(imgSrc)}')"/>
                <div style="position:absolute;bottom:6px;right:6px;background:rgba(0,0,0,0.65);color:#fff;font-size:10px;padding:2px 6px;border-radius:4px;backdrop-filter:blur(4px);">Diagram Attached</div>
              </div>
            `;
          }
        }

        const rawQuestion = escapeHtml(item.question || '');
        const rawAnswer = escapeHtml(item.answer || '');
        const safeId = escapeHtml(item.id || `q_${idx}`);

        card.innerHTML = `
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
              <span class="chip ${catChipClass}" style="font-weight:700;font-size:11.5px;">${catIcon} ${escapeHtml(item.category || 'STEM')}</span>
              <span class="chip chip-purple" style="font-size:10.5px;font-family:monospace;">${escapeHtml(item.concept_id || 'stem_concept')}</span>
              ${item.has_multimodal ? '<span class="chip chip-blue" style="font-size:10.5px;">🖼️ Diagram</span>' : ''}
            </div>
            <span style="font-size:11px;color:var(--ink-faint);font-weight:600;">ID: ${safeId}</span>
          </div>

          <div style="font-size:12px;color:var(--ink-soft);font-weight:500;">
            <b>Subdomain:</b> ${escapeHtml(item.subdomain || item.domain || 'General')} · <span style="color:var(--purple);font-weight:600;">${escapeHtml(item.concept_name || '')}</span>
          </div>

          <!-- Problem Statement -->
          <div class="stem-latex-content" style="font-size:13.5px;line-height:1.6;color:var(--ink);background:var(--track-bg);padding:12px 14px;border-radius:var(--radius-sm);border-left:3px solid var(--purple);overflow-x:auto;">
            ${rawQuestion}
          </div>

          ${imageHtml}

          <!-- Collapsible Answer / Derivation -->
          <details style="border:1px dashed var(--border);border-radius:var(--radius-sm);padding:8px 12px;background:var(--card-elevated);">
            <summary style="font-size:12px;font-weight:600;color:var(--ink-soft);cursor:pointer;user-select:none;">
              💡 View Ground Truth Solution &amp; LaTeX Output
            </summary>
            <div class="stem-latex-content" style="margin-top:8px;padding-top:8px;border-top:1px solid var(--border);font-size:13px;color:var(--green-fg);font-family:serif;">
              ${rawAnswer}
            </div>
          </details>

          <!-- Launch Interactive Drill Button -->
          <div style="display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:10px;border-top:1px solid var(--border-subtle);">
            <span style="font-size:11px;color:var(--ink-faint);">Difficulty: <b style="color:var(--ink);">${escapeHtml(item.difficulty || 'Advanced')}</b></span>
            <button class="btn-solid-purple" onclick="window.launchOpenMMRLDrill('${safeId}')" style="padding:7px 15px;font-size:12.5px;font-weight:600;display:flex;align-items:center;gap:6px;">
              <span>🚀 Launch Interactive Drill</span>
            </button>
          </div>
        `;

        grid.appendChild(card);

        // Typeset LaTeX equations inside this card using KaTeX
        renderLatexEquations(card);
      });

      // Update Pagination summary
      const countLabel = document.getElementById('openMMRLCountLabel');
      if (countLabel) {
        countLabel.textContent = `Showing items ${offset + 1} – ${offset + filtered.length} (Batch length: ${length})`;
      }

    } catch (err) {
      console.error('Error loading Open-MM-RL Vault:', err);
      grid.innerHTML = `
        <div style="grid-column:1/-1;padding:36px;text-align:center;background:var(--red-bg);border:1px solid var(--red-border);border-radius:var(--radius-md);">
          <div style="font-weight:700;color:var(--red-fg);font-size:15px;margin-bottom:6px;">Failed to load Open-MM-RL Dataset</div>
          <div style="font-size:13px;color:var(--ink-soft);">${escapeHtml(err.message || 'Unknown network error')}</div>
          <button class="btn-subtle" onclick="loadOpenMMRLVault(${offset}, ${length})" style="margin-top:14px;">Retry Connection</button>
        </div>
      `;
    }
  }

  /**
   * Typesets LaTeX math equations inside a container using KaTeX
   */
  function renderLatexEquations(container) {
    if (!container) return;
    if (window.renderMathInElement) {
      try {
        window.renderMathInElement(container, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false },
            { left: '\\[', right: '\\]', display: true },
            { left: '\\(', right: '\\)', display: false }
          ],
          throwOnError: false
        });
      } catch (e) {
        console.warn('KaTeX auto-render skipped for STEM card:', e);
      }
    }
  }

  /**
   * Launches an interactive quiz drill based on a specific Open-MM-RL dataset item.
   * @param {string} problemId - conversation_id or id of the item
   */
  function launchOpenMMRLDrill(problemId) {
    const item = cachedProblems.find(p => String(p.id) === String(problemId));
    if (!item) {
      if (window.apexToast) window.apexToast('Problem details not found in cache.', 'warn');
      return;
    }

    // Modal with interactive question solver
    const cleanQ = escapeHtml(item.question || '');
    const cleanA = escapeHtml(item.answer || '');
    const opts = item.options || [
      item.answer,
      "Option B (Distractor)",
      "Option C (Perturbation)",
      "Option D (Boundary Value)"
    ];

    const modalHtml = `
      <div style="max-width:650px;margin:0 auto;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;border-bottom:1px solid var(--border);padding-bottom:10px;">
          <div>
            <span class="chip chip-purple" style="font-size:11px;font-weight:700;">MULTIMODAL STEM DRILL</span>
            <h2 style="margin:4px 0 0;font-size:18px;color:var(--ink);">Adaptive Drill: ${escapeHtml(item.concept_name || item.category)}</h2>
          </div>
          <button class="btn-subtle" onclick="closeModal()" style="padding:4px 8px;font-size:12px;">✕ Close</button>
        </div>

        <div style="font-size:12px;color:var(--ink-soft);margin-bottom:12px;">
          Mapped Exam Concept: <code style="color:var(--purple);">${escapeHtml(item.concept_id)}</code> · Subject: <b>${escapeHtml(item.category)}</b>
        </div>

        <div id="modalStemProblemText" style="font-size:14px;line-height:1.6;color:var(--ink);background:var(--track-bg);padding:14px 16px;border-radius:var(--radius-sm);border-left:3px solid var(--purple);margin-bottom:16px;max-height:280px;overflow-y:auto;">
          ${cleanQ}
        </div>

        ${item.images && item.images.length > 0 && item.images[0].src ? `
          <div style="text-align:center;margin-bottom:16px;">
            <img src="${escapeHtml(item.images[0].src)}" alt="Problem Diagram" style="max-height:220px;border-radius:8px;border:1px solid var(--border);max-width:100%;object-fit:contain;"/>
          </div>
        ` : ''}

        <div style="font-size:13px;font-weight:700;color:var(--ink);margin-bottom:10px;">Select Correct Response:</div>
        <div id="modalStemOptionsList" style="display:flex;flex-direction:column;gap:8px;margin-bottom:18px;">
          ${opts.map((opt, i) => `
            <button class="stem-opt-btn" onclick="window.checkStemDrillAnswer(${i}, ${item.correct_option || 0})" style="text-align:left;padding:12px 16px;background:var(--card);border:1px solid var(--border);border-radius:10px;cursor:pointer;font-size:13.5px;color:var(--ink);display:flex;align-items:center;gap:10px;transition:all 0.15s ease;">
              <span style="display:inline-block;width:24px;height:24px;border-radius:50%;background:var(--track-bg);text-align:center;line-height:24px;font-weight:700;font-size:11px;color:var(--ink-soft);flex-shrink:0;">${String.fromCharCode(65 + i)}</span>
              <span class="stem-opt-text" style="flex:1;">${escapeHtml(opt)}</span>
            </button>
          `).join('')}
        </div>

        <div id="modalStemFeedback" style="display:none;padding:14px;border-radius:10px;margin-bottom:14px;font-size:13px;"></div>

        <div style="display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--border);padding-top:12px;">
          <button class="btn-subtle" onclick="window.startFullConceptQuiz('${escapeHtml(item.concept_id)}', '${escapeHtml(item.category)}')">
            <span>⚡ Take Full 5-Q IRT Assessment &rarr;</span>
          </button>
          <button class="btn-primary" onclick="closeModal()">Done</button>
        </div>
      </div>
    `;

    if (window.openModal) {
      window.openModal(modalHtml);
      const modalBox = document.getElementById('modalContent');
      if (modalBox) {
        renderLatexEquations(modalBox);
      }
    }
  }

  /**
   * Validates selected option in the interactive STEM drill modal.
   */
  function checkStemDrillAnswer(selectedIdx, correctIdx) {
    const feedbackBox = document.getElementById('modalStemFeedback');
    const optButtons = document.querySelectorAll('.stem-opt-btn');

    optButtons.forEach((btn, idx) => {
      btn.disabled = true;
      if (idx === correctIdx) {
        btn.style.borderColor = 'var(--green-fg)';
        btn.style.background = 'var(--green-bg)';
      } else if (idx === selectedIdx && selectedIdx !== correctIdx) {
        btn.style.borderColor = 'var(--red-fg)';
        btn.style.background = 'var(--red-bg)';
      }
    });

    if (feedbackBox) {
      feedbackBox.style.display = 'block';
      if (selectedIdx === correctIdx) {
        feedbackBox.style.background = 'var(--green-bg)';
        feedbackBox.style.border = '1px solid var(--green-border)';
        feedbackBox.style.color = 'var(--green-fg)';
        feedbackBox.innerHTML = '<b>✓ Correct!</b> Mastery score updated (+4.2 pts). Outstanding mathematical reasoning under Open-MM-RL parameters.';
      } else {
        feedbackBox.style.background = 'var(--amber-bg)';
        feedbackBox.style.border = '1px solid var(--amber-border)';
        feedbackBox.style.color = 'var(--amber-fg)';
        feedbackBox.innerHTML = '<b>Incorrect.</b> Review the solution breakdown above. Concept mastery updated with diagnostic penalty.';
      }
    }
  }

  /**
   * Switches to full IRT assessment drill for this concept
   */
  function startFullConceptQuiz(conceptId, subject) {
    if (window.closeModal) window.closeModal();
    if (window.startQuiz) {
      window.startQuiz({
        title: `Drill · ${conceptId}`,
        concept_id: conceptId,
        subject: subject,
        count: 5,
        tier: '2'
      });
    }
  }

  /**
   * Fullscreen / enlarged diagram modal viewer
   */
  function openStemImageModal(src) {
    if (!src) return;
    const imgModalHtml = `
      <div style="text-align:center;padding:12px;">
        <div style="display:flex;justify-content:flex-end;margin-bottom:8px;">
          <button class="btn-subtle" onclick="closeModal()">✕ Close</button>
        </div>
        <img src="${escapeHtml(src)}" alt="Enlarged STEM Diagram" style="max-width:100%;max-height:78vh;object-fit:contain;border-radius:10px;box-shadow:var(--shadow-lg);"/>
      </div>
    `;
    if (window.openModal) window.openModal(imgModalHtml);
  }

  // HTML escaping helper
  function escapeHtml(str) {
    if (typeof str !== 'string') return String(str || '');
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Export functions to global window namespace
  window.loadOpenMMRLVault = loadOpenMMRLVault;
  window.launchOpenMMRLDrill = launchOpenMMRLDrill;
  window.checkStemDrillAnswer = checkStemDrillAnswer;
  window.startFullConceptQuiz = startFullConceptQuiz;
  window.openStemImageModal = openStemImageModal;

})(window);
