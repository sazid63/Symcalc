/**
 * Calculas - University-level calculus solver frontend
 */

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
        subtitle: 'Solve ODEs of the form y\'\' = f(x, y, y\', ...)',
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

let currentOp = 'derivative';
let history = [];
let examplesCache = {};

// ============ INIT ============

document.addEventListener('DOMContentLoaded', () => {
    initOpButtons();
    initForm();
    initHeaderActions();
    setOperation('derivative');
    loadExamples('derivative');
});

function initOpButtons() {
    document.querySelectorAll('.op-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const op = btn.dataset.op;
            document.querySelectorAll('.op-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            setOperation(op);
        });
    });
}

function initForm() {
    document.getElementById('calc-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await solve();
    });
    document.getElementById('clear-btn').addEventListener('click', clearForm);
    document.getElementById('examples-btn').addEventListener('click', toggleExamples);
    document.getElementById('copy-btn').addEventListener('click', copyResult);
    document.getElementById('copy-latex-btn').addEventListener('click', copyLaTeX);
}

function initHeaderActions() {
    document.getElementById('history-toggle').addEventListener('click', () => {
        const drawer = document.getElementById('history-drawer');
        drawer.hidden = !drawer.hidden;
    });
    document.getElementById('history-clear').addEventListener('click', clearHistory);
    document.getElementById('help-toggle').addEventListener('click', () => {
        document.getElementById('help-modal').hidden = false;
    });
    document.querySelectorAll('.modal-close, #help-modal').forEach(el => {
        el.addEventListener('click', (e) => {
            if (e.target === el || el.classList.contains('modal-close')) {
                document.getElementById('help-modal').hidden = true;
            }
        });
    });
}

function setOperation(op) {
    currentOp = op;
    const info = OPERATIONS[op];
    document.getElementById('op-title').textContent = info.title;
    document.getElementById('op-subtitle').textContent = info.subtitle;
    
    // Clear result and error
    document.getElementById('result-panel').hidden = true;
    document.getElementById('error-panel').hidden = true;
    
    // Build extra fields
    const container = document.getElementById('extra-fields');
    container.innerHTML = '';
    info.fields.forEach(field => {
        const div = document.createElement('div');
        div.className = 'form-field';
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
            if (field.default) input.value = field.default;
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
    
    // Load examples
    loadExamples(op);
}

function getFormData() {
    const data = {
        operation: currentOp,
        params: {
            expression: document.getElementById('input-expression').value,
        }
    };
    
    const info = OPERATIONS[currentOp];
    info.fields.forEach(field => {
        const el = document.getElementById(`input-${field.id}`);
        if (el) {
            data.params[field.id] = el.value;
        }
    });
    
    // Special handling
    if (currentOp === 'partial_derivative') {
        data.params.variables_list = data.params.variables_list
            .split(',')
            .map(s => s.trim())
            .filter(s => s);
    }
    
    if (currentOp === 'gradient' || currentOp === 'hessian' || 
        currentOp === 'critical_points' || currentOp === 'laplacian') {
        data.params.variables_list = data.params.variables_list
            .split(',')
            .map(s => s.trim())
            .filter(s => s);
    }
    
    if (currentOp === 'divergence') {
        data.params.variables_list = data.params.variables_list
            .split(',')
            .map(s => s.trim())
            .filter(s => s);
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
        if (data.params.lim0_var) {
            limits.push({
                variable: data.params.lim0_var,
                lower: data.params.lim0_low,
                upper: data.params.lim0_high
            });
        }
        if (data.params.lim1_var) {
            limits.push({
                variable: data.params.lim1_var,
                lower: data.params.lim1_low,
                upper: data.params.lim1_high
            });
        }
        if (data.params.lim2_var && data.params.lim2_var !== '(none)') {
            limits.push({
                variable: data.params.lim2_var,
                lower: data.params.lim2_low,
                upper: data.params.lim2_high
            });
        }
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

async function solve() {
    const data = getFormData();
    
    if (!data.params.expression) {
        showError('Please enter an expression');
        return;
    }
    
    setButtonLoading(true);
    
    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResult(result);
            addToHistory(data, result);
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError(`Network error: ${error.message}`);
    } finally {
        setButtonLoading(false);
    }
}

function displayResult(result) {
    document.getElementById('result-panel').hidden = false;
    document.getElementById('error-panel').hidden = true;
    
    const mathDiv = document.getElementById('result-math');
    const plainDiv = document.getElementById('result-plain');
    
    // Try to render with KaTeX
    if (window.katex && result.latex) {
        try {
            katex.render(result.latex, mathDiv, {
                displayMode: true,
                throwOnError: false
            });
            plainDiv.hidden = true;
        } catch (e) {
            mathDiv.hidden = true;
            plainDiv.hidden = false;
            plainDiv.textContent = result.result;
        }
    } else {
        mathDiv.hidden = true;
        plainDiv.hidden = false;
        plainDiv.textContent = result.result;
    }
    
    // Display steps
    const stepsDiv = document.getElementById('result-steps');
    const stepsList = document.getElementById('steps-list');
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
}

function showError(message) {
    document.getElementById('error-panel').hidden = false;
    document.getElementById('result-panel').hidden = true;
    document.getElementById('error-message').textContent = message;
}

function setButtonLoading(loading) {
    const btn = document.getElementById('solve-btn');
    const label = btn.querySelector('.btn-label');
    const spinner = btn.querySelector('.btn-spinner');
    
    if (loading) {
        label.textContent = 'Computing...';
        spinner.hidden = false;
        btn.disabled = true;
    } else {
        label.textContent = 'Solve';
        spinner.hidden = true;
        btn.disabled = false;
    }
}

function clearForm() {
    document.getElementById('input-expression').value = '';
    document.getElementById('result-panel').hidden = true;
    document.getElementById('error-panel').hidden = true;
}

async function toggleExamples() {
    const container = document.getElementById('examples-container');
    
    if (container.hidden) {
        const examples = await loadExamples(currentOp);
        if (examples && examples.length > 0) {
            container.hidden = false;
            renderExamples(examples);
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
        return [];
    }
}

function renderExamples(examples) {
    const container = document.getElementById('examples-container');
    container.innerHTML = '';
    
    examples.forEach(example => {
        const item = document.createElement('div');
        item.className = 'example-item';
        item.innerHTML = `
            <div class="example-desc">${example.description}</div>
            <div class="example-expr">${escapeHtml(example.expression)}</div>
        `;
        item.addEventListener('click', () => {
            applyExample(example);
            container.hidden = true;
        });
        container.appendChild(item);
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function applyExample(example) {
    // Clear current form
    clearForm();
    
    // Set expression
    document.getElementById('input-expression').value = example.expression;
    
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
    }
}

// ============ HISTORY ============

function addToHistory(data, result) {
    const entry = {
        timestamp: new Date().toISOString(),
        operation: data.operation,
        expression: data.params.expression,
        result: result.result.substring(0, 100),
        params: data.params
    };
    
    history.unshift(entry);
    if (history.length > 50) history.pop();
    
    renderHistory();
}

function renderHistory() {
    const list = document.getElementById('history-list');
    list.innerHTML = '';
    
    history.forEach((entry, index) => {
        const item = document.createElement('div');
        item.className = 'history-item';
        item.innerHTML = `
            <div class="history-op">${entry.operation}</div>
            <div class="history-expr">${escapeHtml(entry.expression)}</div>
            <div class="history-result">${escapeHtml(entry.result)}</div>
        `;
        item.addEventListener('click', () => {
            restoreFromHistory(entry);
            document.getElementById('history-drawer').hidden = true;
        });
        list.appendChild(item);
    });
}

function restoreFromHistory(entry) {
    // Switch to the operation
    document.querySelectorAll('.op-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.op === entry.operation);
    });
    setOperation(entry.operation);
    
    // Set values
    document.getElementById('input-expression').value = entry.expression;
    
    setTimeout(() => {
        const info = OPERATIONS[entry.operation];
        info.fields.forEach(field => {
            const el = document.getElementById(`input-${field.id}`);
            if (el && entry.params[field.id] !== undefined) {
                el.value = entry.params[field.id];
            }
        });
        
        // Handle special fields
        if (entry.params.variables_list && document.getElementById('input-variables_list')) {
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
    }, 10);
}

function clearHistory() {
    history = [];
    renderHistory();
}

// ============ COPY FUNCTIONS ============

function copyResult() {
    const text = document.getElementById('result-plain').hidden 
        ? document.getElementById('result-math').textContent
        : document.getElementById('result-plain').textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

function copyLaTeX() {
    // Re-fetch to get LaTeX
    fetch('/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(getFormData())
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            navigator.clipboard.writeText(data.latex).then(() => {
                alert('LaTeX copied to clipboard!');
            });
        }
    });
}