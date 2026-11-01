/**
 * Calculas — University-level calculus solver frontend (v2)
 *
 * Upgrades over v1:
 *  - Toast notification system (replaces alert())
 *  - Mobile sidebar drawer with overlay + hamburger toggle
 *  - Keyboard shortcuts (Ctrl/Cmd+Enter, Ctrl/Cmd+K, Escape)
 *  - History persisted to localStorage (survives page reloads)
 *  - Copy buttons show animated "Copied ✓" state
 *  - Copy LaTeX uses cached last result instead of re-fetching
 *  - Better error classification (network / parse / server)
 *  - Staggered field animations, header shadow on scroll
 *  - Reduced-motion aware, debounced scroll listener
 */

'use strict';

/* ============================================================
   Operation definitions
   ============================================================ */
const OPERATIONS = {
    derivative: {
        title: 'Derivative',
        subtitle: 'Compute the derivative of a function',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'order', label: 'Order', type: 'number', default: 1, min: 1, max: 10, colSpan: 1 },
        ],
    },
    integral: {
        title: 'Integral',
        subtitle: 'Compute indefinite or definite integral',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'lower', label: 'Lower bound (∅ = indefinite)', type: 'text', placeholder: 'e.g. 0, -oo', colSpan: 1 },
            { id: 'upper', label: 'Upper bound', type: 'text', placeholder: 'e.g. 1, oo', colSpan: 1 },
        ],
    },
    limit: {
        title: 'Limit',
        subtitle: 'Evaluate limits, including one-sided and at infinity',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'point', label: 'Approach point', type: 'text', default: '0', placeholder: 'e.g. 0, oo, -oo, pi', colSpan: 1 },
            { id: 'direction', label: 'Direction', type: 'select', options: ['+-', '+', '-'], default: '+-', colSpan: 1 },
        ],
    },
    series: {
        title: 'Series Expansion',
        subtitle: 'Taylor / Maclaurin series about a point',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'point', label: 'Expansion point', type: 'text', default: '0', colSpan: 1 },
            { id: 'terms', label: 'Number of terms', type: 'number', default: 6, min: 1, max: 30, colSpan: 1 },
        ],
    },
    taylor: {
        title: 'Taylor Series',
        subtitle: 'Same as Series Expansion (alias)',
        fields: [],
    },
    tangent_line: {
        title: 'Tangent Line',
        subtitle: 'Equation of the tangent line at a point',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'point', label: 'Point (x₀)', type: 'text', default: '1', colSpan: 1 },
        ],
    },
    arc_length: {
        title: 'Arc Length',
        subtitle: 'Length of a curve y = f(x) over [a, b]',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'a', label: 'Lower bound a', type: 'text', default: '0', colSpan: 1 },
            { id: 'b', label: 'Upper bound b', type: 'text', default: '1', colSpan: 1 },
        ],
    },
    volume_revolution: {
        title: 'Solid of Revolution',
        subtitle: 'Volume by disc / shell method',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'a', label: 'Lower bound a', type: 'text', default: '0', colSpan: 1 },
            { id: 'b', label: 'Upper bound b', type: 'text', default: '1', colSpan: 1 },
            { id: 'axis', label: 'Axis of revolution', type: 'select', options: ['x', 'y'], default: 'x', colSpan: 1 },
        ],
    },
    surface_area: {
        title: 'Surface of Revolution',
        subtitle: 'Surface area by rotation',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'a', label: 'Lower bound a', type: 'text', default: '0', colSpan: 1 },
            { id: 'b', label: 'Upper bound b', type: 'text', default: '1', colSpan: 1 },
            { id: 'axis', label: 'Axis of revolution', type: 'select', options: ['x', 'y'], default: 'x', colSpan: 1 },
        ],
    },
    improper_integral: {
        title: 'Improper Integral',
        subtitle: 'Integrals with infinite bounds or singularities',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'lower', label: 'Lower bound (∅ = -∞)', type: 'text', default: '0', colSpan: 1 },
            { id: 'upper', label: 'Upper bound (∅ = +∞)', type: 'text', default: 'oo', colSpan: 1 },
        ],
    },
    partial_derivative: {
        title: 'Partial Derivative',
        subtitle: 'Partial derivatives of multivariable functions',
        fields: [
            { id: 'variables_list', label: 'Differentiate with respect to (comma-separated)', type: 'text', default: 'x', placeholder: 'e.g. x, y or x, x, y for ∂³/∂x²∂y', colSpan: 2 },
        ],
    },
    gradient: {
        title: 'Gradient',
        subtitle: 'Gradient vector ∇f',
        fields: [
            { id: 'variables_list', label: 'Variables (comma-separated)', type: 'text', default: 'x, y', colSpan: 2 },
        ],
    },
    hessian: {
        title: 'Hessian Matrix',
        subtitle: 'Matrix of second partial derivatives',
        fields: [
            { id: 'variables_list', label: 'Variables (comma-separated)', type: 'text', default: 'x, y', colSpan: 2 },
        ],
    },
    critical_points: {
        title: 'Critical Points',
        subtitle: 'Solve ∇f = 0 for critical points',
        fields: [
            { id: 'variables_list', label: 'Variables (comma-separated)', type: 'text', default: 'x, y', colSpan: 2 },
        ],
    },
    laplacian: {
        title: 'Laplacian',
        subtitle: '∇²f = sum of unmixed second partials',
        fields: [
            { id: 'variables_list', label: 'Variables (comma-separated)', type: 'text', default: 'x, y', colSpan: 2 },
        ],
    },
    divergence: {
        title: 'Divergence',
        subtitle: '∇·F for a vector field F',
        fields: [
            { id: 'component_0', label: 'Component 1 (P)', type: 'text', default: 'x', colSpan: 1 },
            { id: 'component_1', label: 'Component 2 (Q)', type: 'text', default: 'y', colSpan: 1 },
            { id: 'component_2', label: 'Component 3 (R)', type: 'text', default: '0', colSpan: 1 },
            { id: 'variables_list', label: 'Variables (comma-separated)', type: 'text', default: 'x, y, z', colSpan: 2 },
        ],
    },
    curl: {
        title: 'Curl',
        subtitle: '∇×F for a 3D vector field F',
        fields: [
            { id: 'component_0', label: 'Component 1 (P)', type: 'text', default: '-y', colSpan: 1 },
            { id: 'component_1', label: 'Component 2 (Q)', type: 'text', default: 'x', colSpan: 1 },
            { id: 'component_2', label: 'Component 3 (R)', type: 'text', default: '0', colSpan: 1 },
        ],
    },
    multiple_integral: {
        title: 'Multiple Integral',
        subtitle: 'Double / triple integrals with ordered limits',
        fields: [
            { id: 'lim0_var', label: 'Inner var', type: 'select', options: ['x', 'y', 'z', 't'], default: 'x', colSpan: 1 },
            { id: 'lim0_low', label: 'Inner lower', type: 'text', default: '0', colSpan: 1 },
            { id: 'lim0_high', label: 'Inner upper', type: 'text', default: '1', colSpan: 1 },
            { id: 'lim1_var', label: 'Middle var', type: 'select', options: ['x', 'y', 'z', 't'], default: 'y', colSpan: 1 },
            { id: 'lim1_low', label: 'Middle lower', type: 'text', default: '0', colSpan: 1 },
            { id: 'lim1_high', label: 'Middle upper', type: 'text', default: '1', colSpan: 1 },
            { id: 'lim2_var', label: 'Outer var (∅ = none)', type: 'select', options: ['(none)', 'x', 'y', 'z', 't'], default: '(none)', colSpan: 1 },
            { id: 'lim2_low', label: 'Outer lower', type: 'text', default: '0', disabled: true, colSpan: 1 },
            { id: 'lim2_high', label: 'Outer upper', type: 'text', default: '1', disabled: true, colSpan: 1 },
        ],
    },
    ode: {
        title: 'Differential Equation',
        subtitle: "Solve ODEs of the form y'' = f(x, y, y', ...)",
        fields: [
            { id: 'function', label: 'Dependent variable', type: 'select', options: ['y', 'u', 'f'], default: 'y', colSpan: 1 },
            { id: 'ic', label: 'Initial conditions (optional)', type: 'text', placeholder: 'e.g. y(0)=1', colSpan: 2 },
        ],
    },
    residue: {
        title: 'Residue',
        subtitle: 'Residue of a complex function at a point',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['z', 'x', 'w'], default: 'z', colSpan: 1 },
            { id: 'point', label: 'Point (z₀)', type: 'text', default: 'I', placeholder: 'e.g. I, 0, -I', colSpan: 1 },
        ],
    },
    fourier_series: {
        title: 'Fourier Series',
        subtitle: 'Compute a₀, aₙ, bₙ coefficients',
        fields: [
            { id: 'variable', label: 'Variable', type: 'select', options: ['x', 't', 'y'], default: 'x', colSpan: 1 },
            { id: 'period', label: 'Period', type: 'text', default: '2*pi', colSpan: 1 },
            { id: 'terms', label: 'Number of terms', type: 'number', default: 5, min: 1, max: 20, colSpan: 1 },
        ],
    },
    laplace: {
        title: 'Laplace Transform',
        subtitle: 'F(s) = ℒ{f(t)}',
        fields: [
            { id: 't_var', label: 'Time variable', type: 'select', options: ['t', 'x', 'y'], default: 't', colSpan: 1 },
            { id: 's_var', label: 'Frequency variable', type: 'select', options: ['s', 'w', 'p'], default: 's', colSpan: 1 },
        ],
    },
    inverse_laplace: {
        title: 'Inverse Laplace Transform',
        subtitle: 'f(t) = ℒ⁻¹{F(s)}',
        fields: [
            { id: 't_var', label: 'Time variable', type: 'select', options: ['t', 'x', 'y'], default: 't', colSpan: 1 },
            { id: 's_var', label: 'Frequency variable', type: 'select', options: ['s', 'w', 'p'], default: 's', colSpan: 1 },
        ],
    },
};

/* ============================================================
   State
   ============================================================ */
let currentOp = 'derivative';
let history = [];
let examplesCache = {};
let lastResult = null;          // last successful API result (caches LaTeX)
let isSolving = false;

const HISTORY_KEY = 'calculas-history';
const HISTORY_MAX = 50;

/* Cached DOM references — resolved once, used everywhere */
const els = {};

function cacheDom() {
    const ids = [
        'app-header', 'sidebar', 'sidebar-overlay', 'mobile-menu-btn',
        'calc-form', 'input-expression', 'extra-fields', 'solve-btn',
        'clear-btn', 'examples-btn', 'examples-container',
        'op-title', 'op-subtitle',
        'result-panel', 'result-math', 'result-plain', 'result-steps',
        'steps-list', 'error-panel', 'error-message',
        'copy-btn', 'copy-latex-btn',
        'history-drawer', 'history-list', 'history-clear', 'history-toggle',
        'help-modal', 'help-toggle', 'toast-container',
    ];
    ids.forEach(id => { els[id] = document.getElementById(id); });
}

/* ============================================================
   Helpers
   ============================================================ */

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text ?? '';
    return div.innerHTML;
}

/** Debounce utility for scroll/resize handlers */
function debounce(fn, wait) {
    let t;
    return function (...args) {
        clearTimeout(t);
        t = setTimeout(() => fn.apply(this, args), wait);
    };
}

/* ============================================================
   Toast notifications (replaces alert())
   ============================================================ */

function showToast(message, type = 'info', duration = 2600) {
    const container = els['toast-container'];
    if (!container) return;

    const icons = { success: '✓', error: '✕', info: 'ℹ' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.setAttribute('role', 'status');
    toast.innerHTML =
        `<span class="toast-icon">${icons[type] || 'ℹ'}</span>` +
        `<span class="toast-text">${escapeHtml(message)}</span>`;
    container.appendChild(toast);

    // Auto-dismiss
    setTimeout(() => {
        toast.classList.add('out');
        toast.addEventListener('animationend', () => toast.remove(), { once: true });
    }, duration);

    // Cap at 4 visible toasts
    while (container.children.length > 4) {
        container.firstChild.remove();
    }
}

/* ============================================================
   INIT
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    cacheDom();
    initOpButtons();
    initForm();
    initHeaderActions();
    initMobileSidebar();
    initKeyboardShortcuts();
    initHeaderScroll();
    loadHistory();
    setOperation('derivative');
    loadExamples('derivative');
});

function initOpButtons() {
    document.querySelectorAll('.op-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const op = btn.dataset.op;
            if (op === currentOp) return;
            document.querySelectorAll('.op-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            setOperation(op);
            closeMobileSidebar();
        });
    });
}

function initForm() {
    els['calc-form'].addEventListener('submit', async (e) => {
        e.preventDefault();
        await solve();
    });
    els['clear-btn'].addEventListener('click', clearForm);
    els['examples-btn'].addEventListener('click', toggleExamples);
    els['copy-btn'].addEventListener('click', () => copyResult(false));
    els['copy-latex-btn'].addEventListener('click', () => copyResult(true));
}

function initHeaderActions() {
    els['history-toggle'].addEventListener('click', () => {
        const drawer = els['history-drawer'];
        drawer.hidden = !drawer.hidden;
    });
    els['history-clear'].addEventListener('click', clearHistory);

    els['help-toggle'].addEventListener('click', openHelpModal);

    // Close modal on backdrop click or close button
    els['help-modal'].addEventListener('click', (e) => {
        if (e.target === els['help-modal'] || e.target.closest('.modal-close')) {
            closeHelpModal();
        }
    });
}

/* ---- Mobile sidebar ---- */

function initMobileSidebar() {
    const mq = window.matchMedia('(max-width: 768px)');
    const sync = () => {
        els['mobile-menu-btn'].hidden = !mq.matches;
        if (!mq.matches) closeMobileSidebar();
    };
    sync();
    mq.addEventListener('change', sync);

    els['mobile-menu-btn'].addEventListener('click', () => {
        if (els['sidebar'].classList.contains('open')) closeMobileSidebar();
        else openMobileSidebar();
    });
    els['sidebar-overlay'].addEventListener('click', closeMobileSidebar);
}

function openMobileSidebar() {
    els['sidebar'].classList.add('open');
    els['sidebar-overlay'].classList.add('active');
}

function closeMobileSidebar() {
    els['sidebar'].classList.remove('open');
    els['sidebar-overlay'].classList.remove('active');
}

/* ---- Help modal ---- */

function openHelpModal() {
    els['help-modal'].hidden = false;
    const closeBtn = els['help-modal'].querySelector('.modal-close');
    if (closeBtn) closeBtn.focus();
}

function closeHelpModal() {
    els['help-modal'].hidden = true;
}

/* ---- Keyboard shortcuts ---- */

function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Escape closes modals/drawers
        if (e.key === 'Escape') {
            if (!els['help-modal'].hidden) { closeHelpModal(); return; }
            if (!els['history-drawer'].hidden) { els['history-drawer'].hidden = true; return; }
            if (els['sidebar'].classList.contains('open')) { closeMobileSidebar(); return; }
        }

        const mod = e.ctrlKey || e.metaKey;
        if (mod && e.key === 'Enter') {
            e.preventDefault();
            solve();
        } else if (mod && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            els['input-expression'].focus();
        }
    });
}

/* ---- Header shadow on scroll ---- */

function initHeaderScroll() {
    const onScroll = () => {
        els['app-header'].classList.toggle('scrolled', window.scrollY > 4);
    };
    window.addEventListener('scroll', debounce(onScroll, 50), { passive: true });
    onScroll();
}

/* ============================================================
   Operation switching
   ============================================================ */

function setOperation(op) {
    currentOp = op;
    const info = OPERATIONS[op];
    if (!info) return;
    els['op-title'].textContent = info.title;
    els['op-subtitle'].textContent = info.subtitle;

    // Clear result and error
    els['result-panel'].hidden = true;
    els['error-panel'].hidden = true;

    // Build extra fields (with staggered fade-in)
    const container = els['extra-fields'];
    container.innerHTML = '';
    info.fields.forEach((field, i) => {
        const div = document.createElement('div');
        div.className = 'form-field';
        div.style.animationDelay = `${i * 40}ms`;
        if (field.colSpan === 2) div.style.gridColumn = 'span 2';

        const label = document.createElement('label');
        label.htmlFor = `input-${field.id}`;
        label.textContent = field.label;
        div.appendChild(label);

        let input;
        if (field.type === 'select') {
            input = document.createElement('select');
            field.options.forEach(opt => {
                const option = document.createElement('option');
                option.value = opt;
                option.textContent = opt;
                if (opt === field.default) option.selected = true;
                input.appendChild(option);
            });
        } else if (field.type === 'number') {
            input = document.createElement('input');
            input.type = 'number';
            input.value = field.default;
            if (field.min !== undefined) input.min = field.min;
            if (field.max !== undefined) input.max = field.max;
        } else {
            input = document.createElement('input');
            input.type = 'text';
            if (field.default !== undefined) input.value = field.default;
            if (field.placeholder) input.placeholder = field.placeholder;
        }
        input.id = `input-${field.id}`;
        if (field.disabled) input.disabled = true;
        div.appendChild(input);
        container.appendChild(div);
    });

    // For multiple integral, handle outer variable disable
    if (op === 'multiple_integral') {
        const lim2Var = document.getElementById('input-lim2_var');
        if (lim2Var) {
            lim2Var.addEventListener('change', () => {
                const isNone = lim2Var.value === '(none)';
                document.getElementById('input-lim2_low').disabled = isNone;
                document.getElementById('input-lim2_high').disabled = isNone;
            });
        }
    }

    // Preload examples
    loadExamples(op);
}

/* ============================================================
   Form data
   ============================================================ */

function splitVarList(str) {
    return String(str || '').split(',').map(s => s.trim()).filter(s => s);
}

function getFormData() {
    const data = {
        operation: currentOp,
        params: {
            expression: els['input-expression'].value,
        }
    };

    const info = OPERATIONS[currentOp];
    info.fields.forEach(field => {
        const el = document.getElementById(`input-${field.id}`);
        if (el) {
            // Send numbers as numbers where the field is numeric
            data.params[field.id] = field.type === 'number'
                ? (el.value === '' ? '' : Number(el.value))
                : el.value;
        }
    });

    // Special handling
    if (currentOp === 'partial_derivative' ||
        currentOp === 'gradient' || currentOp === 'hessian' ||
        currentOp === 'critical_points' || currentOp === 'laplacian') {
        data.params.variables_list = splitVarList(data.params.variables_list);
    }

    if (currentOp === 'divergence') {
        data.params.variables_list = splitVarList(data.params.variables_list);
        data.params.vector_field = [
            data.params.component_0,
            data.params.component_1,
            data.params.component_2
        ].filter(v => v !== '' && v !== undefined);
    }

    if (currentOp === 'curl') {
        data.params.variables_list = ['x', 'y', 'z'];
        data.params.vector_field = [
            data.params.component_0,
            data.params.component_1,
            data.params.component_2
        ].filter(v => v !== '' && v !== undefined);
    }

    if (currentOp === 'multiple_integral') {
        const limits = [];
        ['lim0', 'lim1', 'lim2'].forEach(prefix => {
            const varVal = data.params[`${prefix}_var`];
            if (varVal && varVal !== '(none)') {
                limits.push({
                    variable: varVal,
                    lower: data.params[`${prefix}_low`],
                    upper: data.params[`${prefix}_high`]
                });
            }
        });
        data.params.limits = limits;
    }

    if (currentOp === 'ode') {
        data.params.initial_conditions = parseInitialConditions(data.params.ic);
    }

    return data;
}

function parseInitialConditions(icStr) {
    if (!icStr || icStr.trim() === '') return null;
    const ics = {};
    icStr.split(',').forEach(part => {
        const match = part.trim().match(/^(\w+)\(([^)]+)\)\s*=\s*(.+)$/);
        if (match) {
            ics[match[1]] = match[2];
        }
    });
    return Object.keys(ics).length > 0 ? ics : null;
}

/* ============================================================
   Solve
   ============================================================ */

async function solve() {
    if (isSolving) return;
    const data = getFormData();

    if (!data.params.expression.trim()) {
        showError('Please enter an expression first.');
        els['input-expression'].focus();
        return;
    }

    setButtonLoading(true);
    isSolving = true;

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        let result;
        try {
            result = await response.json();
        } catch (parseErr) {
            throw new Error(`Server returned invalid response (HTTP ${response.status})`);
        }

        if (result.success) {
            lastResult = result;
            displayResult(result);
            addToHistory(data, result);
            showToast('Computation successful', 'success', 1800);
        } else {
            showError(result.error || 'Unknown computation error');
        }
    } catch (error) {
        if (error instanceof TypeError && error.message === 'Failed to fetch') {
            showError('Network error — could not reach the server. Is the app running?');
        } else {
            showError(`Request failed: ${error.message}`);
        }
        console.error('Solve error:', error);
    } finally {
        isSolving = false;
        setButtonLoading(false);
    }
}

/* ============================================================
   Result display
   ============================================================ */

function displayResult(result) {
    els['result-panel'].hidden = false;
    els['error-panel'].hidden = true;

    const mathDiv = els['result-math'];
    const plainDiv = els['result-plain'];
    mathDiv.innerHTML = '';
    plainDiv.textContent = '';

    // Try to render with KaTeX
    let renderedMath = false;
    if (window.katex && result.latex) {
        try {
            katex.render(result.latex, mathDiv, {
                displayMode: true,
                throwOnError: false
            });
            renderedMath = true;
        } catch (e) {
            console.warn('KaTeX render failed, falling back to plain text:', e);
        }
    }
    mathDiv.hidden = !renderedMath;
    plainDiv.hidden = renderedMath;
    plainDiv.textContent = result.result;

    // Display steps
    const stepsDiv = els['result-steps'];
    const stepsList = els['steps-list'];
    stepsList.innerHTML = '';

    if (result.steps && result.steps.length > 0) {
        stepsDiv.hidden = false;
        result.steps.forEach(step => {
            const li = document.createElement('li');
            li.textContent = step;
            stepsList.appendChild(li);
        });
    } else {
        stepsDiv.hidden = true;
    }

    // Smooth scroll to result on small screens
    if (window.matchMedia('(max-width: 768px)').matches) {
        els['result-panel'].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

function showError(message) {
    els['error-panel'].hidden = false;
    els['result-panel'].hidden = true;
    els['error-message'].textContent = message;

    // Re-trigger shake animation
    const panel = els['error-panel'];
    panel.style.animation = 'none';
    void panel.offsetWidth; // force reflow
    panel.style.animation = '';
}

function setButtonLoading(loading) {
    const btn = els['solve-btn'];
    const label = btn.querySelector('.btn-label');
    const spinner = btn.querySelector('.btn-spinner');

    if (loading) {
        label.textContent = 'Computing…';
        spinner.hidden = false;
        btn.disabled = true;
    } else {
        label.textContent = 'Solve';
        spinner.hidden = true;
        btn.disabled = false;
    }
}

function clearForm() {
    els['input-expression'].value = '';
    els['result-panel'].hidden = true;
    els['error-panel'].hidden = true;
    els['input-expression'].focus();
}

/* ============================================================
   Examples
   ============================================================ */

async function toggleExamples() {
    const container = els['examples-container'];

    if (container.hidden) {
        const examples = await loadExamples(currentOp);
        if (examples && examples.length > 0) {
            renderExamples(examples);
            container.hidden = false;
        } else {
            showToast('No examples available for this operation', 'info');
        }
    } else {
        container.hidden = true;
    }
}

async function loadExamples(op) {
    if (examplesCache[op]) {
        return examplesCache[op];
    }

    try {
        const response = await fetch('/api/examples');
        const allExamples = await response.json();
        examplesCache[op] = allExamples[op] || [];
        return examplesCache[op];
    } catch (e) {
        console.warn('Failed to load examples:', e);
        return [];
    }
}

function renderExamples(examples) {
    const container = els['examples-container'];
    container.innerHTML = '';

    examples.forEach(example => {
        const item = document.createElement('div');
        item.className = 'example-item';
        item.setAttribute('role', 'button');
        item.setAttribute('tabindex', '0');
        item.innerHTML = `
            <div class="example-desc">${escapeHtml(example.description)}</div>
            <div class="example-expr">${escapeHtml(example.expression || '')}</div>
        `;
        const apply = () => {
            applyExample(example);
            container.hidden = true;
        };
        item.addEventListener('click', apply);
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); apply(); }
        });
        container.appendChild(item);
    });
}

function applyExample(example) {
    clearForm();

    // Set expression
    els['input-expression'].value = example.expression || '';

    // Set operation-specific fields
    const info = OPERATIONS[currentOp];
    info.fields.forEach(field => {
        const el = document.getElementById(`input-${field.id}`);
        if (el && example[field.id] !== undefined) {
            el.value = example[field.id];
        }
    });

    // Handle special fields
    if (example.variables_list) {
        const el = document.getElementById('input-variables_list');
        if (el) el.value = example.variables_list.join(', ');
    }

    if (example.vector_field) {
        const components = example.vector_field;
        if (document.getElementById('input-component_0')) {
            document.getElementById('input-component_0').value = components[0] || '';
            document.getElementById('input-component_1').value = components[1] || '';
            document.getElementById('input-component_2').value = components[2] || '';
        }
    }

    if (example.limits) {
        const limits = example.limits;
        if (limits[0]) {
            document.getElementById('input-lim0_var').value = limits[0].variable;
            document.getElementById('input-lim0_low').value = limits[0].lower;
            document.getElementById('input-lim0_high').value = limits[0].upper;
        }
        if (limits[1]) {
            document.getElementById('input-lim1_var').value = limits[1].variable;
            document.getElementById('input-lim1_low').value = limits[1].lower;
            document.getElementById('input-lim1_high').value = limits[1].upper;
        }
        if (limits[2]) {
            const varEl = document.getElementById('input-lim2_var');
            const lowEl = document.getElementById('input-lim2_low');
            const highEl = document.getElementById('input-lim2_high');
            varEl.value = limits[2].variable;
            lowEl.disabled = false;
            highEl.disabled = false;
            lowEl.value = limits[2].lower;
            highEl.value = limits[2].upper;
        }
    }
}

/* ============================================================
   History (persisted to localStorage)
   ============================================================ */

function loadHistory() {
    try {
        const raw = localStorage.getItem(HISTORY_KEY);
        if (raw) {
            const parsed = JSON.parse(raw);
            if (Array.isArray(parsed)) history = parsed.slice(0, HISTORY_MAX);
        }
    } catch (e) {
        console.warn('Could not restore history from storage:', e);
        history = [];
    }
    renderHistory();
}

function saveHistory() {
    try {
        localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    } catch (e) {
        console.warn('Could not persist history:', e);
    }
}

function addToHistory(data, result) {
    const entry = {
        timestamp: new Date().toISOString(),
        operation: data.operation,
        expression: data.params.expression,
        result: String(result.result).substring(0, 120),
        params: data.params
    };

    history.unshift(entry);
    if (history.length > HISTORY_MAX) history.pop();

    saveHistory();
    renderHistory();
}

function renderHistory() {
    const list = els['history-list'];
    list.innerHTML = '';

    if (history.length === 0) {
        // Empty state handled by CSS ::after pseudo-element
        return;
    }

    history.forEach((entry, index) => {
        const item = document.createElement('div');
        item.className = 'history-item';
        item.setAttribute('role', 'button');
        item.setAttribute('tabindex', '0');
        item.style.animationDelay = `${Math.min(index, 8) * 45}ms`;
        item.innerHTML = `
            <div class="history-op">${escapeHtml(humanizeOp(entry.operation))}</div>
            <div class="history-expr">${escapeHtml(entry.expression)}</div>
            <div class="history-result">${escapeHtml(entry.result)}</div>
        `;
        const restore = () => {
            restoreFromHistory(entry);
            els['history-drawer'].hidden = true;
            showToast('Problem restored from history', 'info', 1600);
        };
        item.addEventListener('click', restore);
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); restore(); }
        });
        list.appendChild(item);
    });
}

function humanizeOp(op) {
    const info = OPERATIONS[op];
    return info ? info.title : op;
}

function restoreFromHistory(entry) {
    // Switch to the operation
    document.querySelectorAll('.op-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.op === entry.operation);
    });
    setOperation(entry.operation);

    // Set values
    els['input-expression'].value = entry.expression;

    // requestAnimationFrame double-tick guarantees fields exist
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            const info = OPERATIONS[entry.operation];
            if (!info) return;
            info.fields.forEach(field => {
                const el = document.getElementById(`input-${field.id}`);
                if (el && entry.params[field.id] !== undefined && entry.params[field.id] !== null) {
                    el.value = entry.params[field.id];
                }
            });

            // Handle special fields
            if (Array.isArray(entry.params.variables_list) && document.getElementById('input-variables_list')) {
                document.getElementById('input-variables_list').value =
                    entry.params.variables_list.join(', ');
            }

            if (entry.params.vector_field) {
                const components = entry.params.vector_field;
                if (document.getElementById('input-component_0')) {
                    document.getElementById('input-component_0').value = components[0] || '';
                    document.getElementById('input-component_1').value = components[1] || '';
                    document.getElementById('input-component_2').value = components[2] || '';
                }
            }
        });
    });
}

function clearHistory() {
    history = [];
    saveHistory();
    renderHistory();
    showToast('History cleared', 'info');
}

/* ============================================================
   Copy functions
   ============================================================ */

async function copyText(text, successMsg) {
    if (!text) {
        showToast('Nothing to copy', 'error');
        return false;
    }
    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
        } else {
            // Fallback for non-secure contexts
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.opacity = '0';
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            ta.remove();
        }
        showToast(successMsg, 'success');
        return true;
    } catch (err) {
        console.error('Copy failed:', err);
        showToast('Copy failed — select the text manually', 'error');
        return false;
    }
}

function currentDisplayText() {
    if (els['result-plain'].hidden) {
        return els['result-math'].textContent || '';
    }
    return els['result-plain'].textContent || '';
}

async function copyResult(isLaTeX) {
    const btn = isLaTeX ? els['copy-latex-btn'] : els['copy-btn'];
    const originalLabel = btn.querySelector('span:last-child');
    const originalText = originalLabel.textContent;

    let text;
    if (isLaTeX) {
        // Use cached last result — no re-fetch needed
        if (!lastResult || !lastResult.latex) {
            showToast('Solve a problem first to copy LaTeX', 'info');
            return;
        }
        text = lastResult.latex;
    } else {
        text = currentDisplayText();
    }

    const ok = await copyText(text, isLaTeX ? 'LaTeX copied to clipboard' : 'Result copied to clipboard');
    if (ok) {
        btn.classList.add('copied');
        originalLabel.textContent = 'Copied ✓';
        setTimeout(() => {
            btn.classList.remove('copied');
            originalLabel.textContent = originalText;
        }, 1600);
    }
}
