/**
 * Medical Imaging Portfolio — project data, metrics, asset detection.
 */

const PROJECTS = [
  {
    id: "dicom-qc",
    tool: "DICOM / pydicom",
    title: "DICOM Ingest, De-ID & QC",
    description:
      "Automated ingestion, PS3.15 de-identification, and QC gates (spacing, HU range, slice count) for AI training cohorts.",
    exportFile: "assets/qc-summary.png",
    screenshotFile: "assets/dicom-import-session.png",
    workflowPath: "../workflows/01-dicom-ingest-qc-workflow.md",
    briefPath: "../projects/01-dicom-ingest-qc.md",
    metricsKey: "qc",
  },
  {
    id: "segment-editor",
    tool: "3D Slicer",
    title: "Expert Segmentation — Segment Editor",
    description:
      "Manual and semi-automatic spleen segmentation with documented window/level, HU ranges, and 3D topology review.",
    exportFile: "assets/spleen-segmentation-overlay.png",
    screenshotFile: "assets/segment-editor-session.png",
    workflowPath: "../workflows/02-segment-editor-workflow.md",
    briefPath: "../projects/02-segment-editor.md",
  },
  {
    id: "ai-loop",
    tool: "nnU-Net / SimpleITK",
    title: "AI Correction Loop",
    description:
      "Human-in-the-loop: AI draft mask → expert correction in Slicer → quantified Dice/HD95 improvement.",
    exportFile: "assets/ai-correction-comparison.png",
    screenshotFile: "assets/ai-correction-comparison.png",
    workflowPath: "../workflows/03-ai-correction-loop-workflow.md",
    briefPath: "../projects/03-ai-correction-loop.md",
    metricsKey: "dice",
  },
  {
    id: "dicom-seg",
    tool: "highdicom",
    title: "DICOM-SEG Export",
    description:
      "Interoperable DICOM-SEG with geometry validation and provenance JSON sidecars for AI research assets.",
    exportFile: "assets/sample-spleen.dcm",
    screenshotFile: "assets/dicom-seg-roundtrip.png",
    workflowPath: "../workflows/04-dicom-seg-export-workflow.md",
    briefPath: "../projects/04-dicom-seg-export.md",
  },
  {
    id: "extension",
    tool: "Slicer Extension",
    title: "MedAssetPipeline Module",
    description:
      "Custom ScriptedLoadableModule: QC panel, Dice validation, one-click DICOM-SEG + provenance export.",
    exportFile: "assets/extension-ui-session.png",
    screenshotFile: "assets/extension-export-demo.png",
    workflowPath: "../workflows/05-slicer-extension-workflow.md",
    briefPath: "../projects/05-slicer-extension.md",
  },
];

const assetStatus = {};

async function checkAsset(url) {
  try {
    const res = await fetch(url, { method: "HEAD" });
    return res.ok;
  } catch {
    return false;
  }
}

async function detectAssets() {
  for (const p of PROJECTS) {
    const exportOk = await checkAsset(p.exportFile);
    const shotOk = await checkAsset(p.screenshotFile);
    assetStatus[p.id] = { export: exportOk, screenshot: shotOk, ready: exportOk && shotOk };
  }
}

function renderProjects() {
  const grid = document.getElementById("project-grid");
  if (!grid) return;

  grid.innerHTML = PROJECTS.map((p) => {
    const status = assetStatus[p.id] || { ready: false };
    const statusClass = status.ready ? "ready" : "pending";
    const statusText = status.ready ? "Ready" : "Run make validate";

    const thumb = status.screenshot
      ? `<img src="${p.screenshotFile}" alt="${p.title}">`
      : `<div class="project-thumb-placeholder"><span class="icon">🩻</span>${p.tool}</div>`;

    const metricSnippet = p.metricsKey === "dice"
      ? `<p class="project-metric" id="card-metric-${p.id}">Dice: —</p>`
      : "";

    return `
      <article class="project-card" data-id="${p.id}">
        <div class="project-thumb">${thumb}</div>
        <div class="project-body">
          <span class="project-status ${statusClass}">${statusText}</span>
          <p class="project-tool">${p.tool}</p>
          <h3 class="project-title">${p.title}</h3>
          <p class="project-desc">${p.description}</p>
          ${metricSnippet}
          <div class="project-links">
            <a class="project-link primary" href="${p.briefPath}">Brief</a>
            <a class="project-link" href="${p.workflowPath}">Workflow</a>
          </div>
        </div>
      </article>`;
  }).join("");
}

function renderWorkflows() {
  const list = document.getElementById("workflow-list");
  if (!list) return;

  list.innerHTML = PROJECTS.map(
    (p) => `
    <li class="workflow-item">
      <div class="workflow-item-info">
        <h3>${p.title}</h3>
        <p>${p.tool} — decision log with technical rationale</p>
      </div>
      <span class="workflow-item-tool">
        <a class="project-link" href="${p.workflowPath}">View doc</a>
      </span>
    </li>`
  ).join("");
}

async function loadMetrics() {
  const panel = document.getElementById("metrics-panel");
  if (!panel) return;

  try {
    const [metricsRes, qcRes] = await Promise.all([
      fetch("assets/segmentation-metrics.json"),
      fetch("assets/qc-report.json"),
    ]);

    const cards = [];

    if (metricsRes.ok) {
      const metrics = await metricsRes.json();
      const agg = metrics.aggregate || {};
      if (agg.mean_dice_ai !== undefined) {
        cards.push({ label: "Mean Dice (AI)", value: agg.mean_dice_ai.toFixed(3) });
      }
      if (agg.mean_dice_corrected !== undefined) {
        cards.push({ label: "Mean Dice (Corrected)", value: agg.mean_dice_corrected.toFixed(3) });
        const el = document.getElementById("card-metric-ai-loop");
        if (el) el.textContent = `Dice: ${agg.mean_dice_corrected.toFixed(3)}`;
      }
    }

    if (qcRes.ok) {
      const qc = await qcRes.json();
      cards.push({ label: "QC Passed", value: `${qc.passed}/${qc.total_cases}` });
    }

    if (cards.length === 0) {
      panel.innerHTML = `<p class="metrics-loading">Run <code>make validate</code> to generate metrics.</p>`;
      return;
    }

    panel.innerHTML = cards
      .map(
        (c) => `
      <div class="metric-card">
        <p class="label">${c.label}</p>
        <p class="value">${c.value}</p>
      </div>`
      )
      .join("");
  } catch {
    panel.innerHTML = `<p class="metrics-loading">Metrics unavailable — run pipeline locally.</p>`;
  }
}

function setUpdatedDate() {
  const el = document.getElementById("portfolio-updated");
  if (el) {
    el.textContent = `Updated: ${new Date().toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" })}`;
  }
}

async function init() {
  setUpdatedDate();
  await detectAssets();
  renderProjects();
  renderWorkflows();
  await loadMetrics();
}

document.addEventListener("DOMContentLoaded", init);
