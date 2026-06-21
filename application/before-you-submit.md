# Before You Submit — Honest Eligibility Check

This kit puts you **ahead of most survey applicants** who only have screenshots or tutorial certificates. It is **not a guarantee** of selection — Micro1-style screening also tests live expertise, availability, and fit for the specific AI research contract.

## What this kit already proves (strong signals)

| Signal | Strength | Evidence |
|--------|----------|----------|
| End-to-end digital asset pipeline | High | `pipeline/medasset/`, `make validate` |
| 3D Slicer extension authorship | High | `extensions/MedAssetPipeline/` |
| Human-in-the-loop AI workflow | High | Project 03, workflow docs, metrics JSON |
| DICOM + provenance awareness | High | de-ID, DICOM-SEG export, sidecars |
| Reproducibility | High | CI, golden metrics, one-command demo |
| Documentation for AI training roles | High | Five workflow decision logs |

## Gaps that can still cost you the role

| Gap | Risk | Fix before submit |
|-----|------|-------------------|
| No **live HTTPS portfolio URL** | Recruiters cannot see your work | Deploy `portfolio/` to GitHub Pages or Netlify |
| **Matplotlib placeholders** instead of real Slicer UI | Looks automated, not hands-on | Replace `portfolio/assets/*-session.png` with actual Slicer screenshots |
| Only **synthetic / 1-case** demo | Undersells advanced experience | Run `make data` for MSD Task09; segment 2–3 real cases |
| No **nnU-Net** run on real weights | "Used nnU-Net" is unsubstantiated | Install nnU-Net v2, run `make infer` on MSD, document in workflow 03 |
| No **3-minute screen recording** | Survey may ask for verbal walkthrough | Record Slicer correction loop + extension export (unlisted YouTube) |
| Generic GitHub URL | Low discoverability | Public repo, README images, CI badge green |

## Realistic outcome

- **Eligibility survey / portfolio review:** This kit is designed to pass — if deployed and personalized.
- **Final selection:** Depends on competition, rate, timezone, and live evaluation tasks. Your workflow docs and extension are differentiators; **real Slicer session evidence** closes the gap between "impressive repo" and "hire this person."

## Minimum bar to submit (30-minute checklist)

- [ ] Name in `portfolio/index.html`
- [ ] `./scripts/check-portfolio.sh` passes
- [ ] Portfolio live at public URL (paste in survey)
- [ ] GitHub repo public with this README
- [ ] At least **one** real 3D Slicer screenshot replaces a pipeline-generated PNG
- [ ] Read `application/survey-prep.md` and practice 3-min AI correction loop talk track

## Stretch moves (top 5% of applicants)

- MONAI Label + Slicer active learning demo (documented in README stretch section)
- Second organ (MSD Task03 Liver) with multi-structure DICOM-SEG export
- Published Slicer extension or fork with install count
- Short Loom/YouTube: clone repo → `make validate` → open extension in Slicer
