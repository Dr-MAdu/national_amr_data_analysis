# Ghana One Health AMR Surveillance: Data Analysis Standards and Guidelines

This document provides detailed coding standards and analysis instructions for Ghana’s One Health AMR surveillance annual report, using the full range of human blood culture isolate data. It emphasizes WHO priority pathogens and clinically significant organisms, aligns with WHO GLASS and CLSI M39 standards, and embeds a One Health perspective. All analysis steps must be automated, reproducible, and well-documented, with clean CSV outputs for each section.

## Data Sources and Preparation

* **Input Data:** Use the standardized blood culture AMR dataset (Data\_Department\_Standardized.csv) covering all years available. Include all patients and specimens in the time series, ensuring the full timeframe is analyzed.
* **Reference Tables:** Load the antimicrobial reference (Antimicrobials\_Data\_Final.csv) and organism reference (Organisms\_Data\_Final.csv) to map WHONET codes to full names, classes, and WHO AWaRe categories. Use these to validate codes and add descriptive fields (drug class, AWaRe category, organism genus/species).
* **Data Cleaning:** Check and correct inconsistent entries (e.g. misspelled organism names, unknown organism codes). Standardize text (e.g. region names, department names) for consistency. Handle missing data explicitly (e.g. mark missing susceptibility results as `NA`).
* **Specimen Filters:** Restrict to human blood culture isolates. Remove any non-blood samples or environmental isolates. Exclude obvious contaminants or non-pathogens if documented (e.g. code “xxx” for no growth, many coagulase-negative staphylococci if not clinically significant).

## Pathogen Prioritization (WHO Priority and Other Key Organisms)

* **WHO Priority Pathogens:** Emphasize analysis of pathogens on the WHO bacterial priority list (2024), which includes critical and high-priority organisms such as carbapenem-resistant *Acinetobacter* spp., ESBL-producing *Enterobacteriaceae* (e.g. *Escherichia coli*, *Klebsiella pneumoniae*), *Salmonella* spp., *Shigella* spp., *Pseudomonas aeruginosa*, *Staphylococcus aureus* (including MRSA), *Neisseria gonorrhoeae*, and others. These should be highlighted in summary tables and graphs.
* **GLASS-AMR Target Organisms:** Align focus with WHO GLASS-AMR; specifically include *Acinetobacter* spp., *E. coli*, *K. pneumoniae*, *Salmonella* spp., *Shigella* spp., *Staphylococcus aureus*, *Streptococcus pneumoniae*, and other fast-growing bacteria. Even if some (e.g. *N. gonorrhoeae*) are rare in blood, ensure consistency with GLASS categories.
* **One Health Context:** Note that *E. coli* is prevalent in humans, animals, and the environment, making it an ideal One Health indicator. Emphasize *E. coli* and other zoonotic or environmental link organisms in analysis and interpretation. Consider human–animal linkages when relevant, even though this dataset is human-only.
* **Clinically Significant Others:** Also report on other common pathogens in blood cultures (e.g. *Enterococcus* spp., *Enterobacter* spp., *Pseudomonas aeruginosa*, *Citrobacter* spp.) to provide context. Prioritize organisms with sufficient sample size (e.g. ≥30 isolates per year for stable estimates).

## International Standards Alignment (WHO GLASS and CLSI M39)

* **GLASS Guidance:** Follow WHO GLASS methodology for surveillance of AMR. Use GLASS definitions where applicable: de-duplicate isolates per patient, classify infection origin (community vs hospital), and calculate AMR indicators. GLASS encourages countries to aim for nationally representative data, but analysis should transparently report the number of sites and isolates. According to WHO, “cases of AMR infection” from blood culture should have AST results de-duplicated and combined with patient data.
* **Strategic Objectives:** Align with GLASS-AMR objectives: harmonize national standards, monitor AMR trends in priority pathogens, and inform WHO models (e.g. Essential Medicines, AWaRe). In particular, use WHO AWaRe categories (Access/Watch/Reserve) to group antibiotics in analysis (as provided in the antimicrobial reference).
* **CLSI M39 Guidelines:** Implement CLSI M39 recommendations for cumulative susceptibility reporting. This includes ensuring methods are reliable and consistent – “if methods… are not reliable and consistent, many important applications… will not be realized”. Follow M39 scope: prepare cumulative antibiograms from final, accurate isolate data. For each facility or the national aggregate, compute routine antibiograms (percent susceptible) for relevant bug–drug combinations. Use M39’s advice on dealing with automated vs manual data sources, intermediate results, and confidence measures.

## Data Validation and Deduplication

* **Reference Validation:** Use the antimicrobial and organism reference files to validate each data record. For example, if an AST column has code “AMK”, confirm it matches *amikacin*. Flag any mismatches or unknown codes. Ensure organism codes match the reference list.
* **Duplicate Records:** Remove duplicate isolates per patient and specimen type per analysis period (e.g. one blood isolate per patient per year) to avoid over-counting. When duplicates exist, keep the first or most clinically relevant isolate (as per CLSI and GLASS recommendations). Document the deduplication rule clearly in the code.
* **Missing and Outlier Handling:** Identify missing values (e.g. absent AST results) and decide treatment (e.g. exclude or impute if justified). Check for out-of-range dates or ages. Validate that age and sex are in plausible formats and ranges. Any errors or corrections should be logged or flagged.
* **Assumptions:** Assume all AST results are final and use current breakpoints. If the data includes intermediate (“I”) results, follow CLSI advice (e.g. M39 suggests how to report intermediate values). Specify how “I” is handled (often grouped with “R” or excluded from % susceptible denominator, per local policy).

## Data Transformation and Analysis Preparation

* **Tidy Format:** Convert data into a tidy format. For each isolate (one row), include: patient ID, date, hospital/region, organism, and susceptibility results for each antibiotic. Generate new columns as needed (e.g. calendar year from specimen date).
* **Merging References:** Join the organism reference to add organism type and common name, and join the antimicrobial reference to tag AWaRe and drug class for each AST column. This enables grouping by antibiotic class and stewardship category.
* **Derived Variables:** Create categorical variables (e.g. age groups, ward type). Compute indicators such as “resistant” (R) or “non-susceptible” (R+I) for each antibiotic. Aggregate AWaRe usage (e.g. count of Access vs Watch antibiotics tested).
* **Documentation:** In the analysis code, comment each transformation step. Keep a log of row counts before/after cleaning for QA. Each transformation script should output a validated, analysis-ready dataset (and save intermediate files if needed) in a reproducible way.

## Analysis and Summary Metrics

* **Isolate and Patient Counts:** Produce tables of total isolates and patients by year, organism, and location (region/hospital/ward). Include both raw counts and incidence rates if denominator data are available. Emphasize trends over the full time range.
* **Resistance Proportions:** For each priority organism–antibiotic pair (based on WHO/GLASS lists), calculate the percentage of isolates that are resistant. For example, compute MRSA% among *S. aureus* and ESBL (3rd‑gen cephalosporin resistance) % among Enterobacterales. Use GLASS indicator definitions where possible. For instance, GLASS defines MRSA by oxacillin/cefoxitin criteria and ESBL E. coli by ceftriaxone/cefotaxime resistance. Report both numerators and denominators.
* **Time Trends:** Plot multi-year trends of key resistance rates and organism frequencies. For example, line graphs of MRSA% and ESBL *E. coli*% by year, or bars of *K. pneumoniae* isolations per year. Statistical methods (e.g. 95% CIs or trend tests) may be included to support significance statements.
* **Summary Tables:** Create pivot tables suitable for report inclusion, such as (a) Total isolates by pathogen and year, (b) Cumulative antibiograms (percent susceptible) for each WHO priority pathogen against a panel of antibiotics, (c) AWaRe-category usage breakdown, and (d) Demographic breakdowns (age/sex distribution of resistant infections). Each table should have clear headers and units.
* **Alignment with WHO/CLSI:** Ensure that computed summaries correspond to international standards. For example, CLSI M39 recommends reporting percent susceptible as the key metric. Similarly, GLASS expects disaggregated data by pathogen, specimen, and origin (community vs hospital) – include these strata if available.

## Visualization Best Practices

* **Clarity and Simplicity:** Use charts that are easy to interpret (bar charts, line plots, stacked bars). Avoid overly complex graphics. Each figure must have a descriptive title, labeled axes, and a legend if needed. For percent resistance, label as “% of isolates resistant”.
* **Color and Accessibility:** Use color palettes that are color-blind–friendly. Do not rely solely on color to differentiate data series (use patterns or labels if possible).
* **Data Integrity:** Do not manipulate scales to exaggerate differences. Include appropriate reference lines (e.g. 0% baseline). Annotate important values or thresholds.
* **Captions and Notes:** Include figure captions or footnotes summarizing the key message (e.g. “Increasing trend in ESBL *E. coli* prevalence” or “Data limited before 2015 due to fewer sites”).
* **Export Formats:** Save visuals in high-resolution PNG or PDF format for the report. Also export any underlying summarized data (as CSV) used for the figure so results can be verified.

## Reproducibility and Documentation

* **Scripted Analysis:** All steps must be coded (no manual editing of tables). Use a version-controlled repository (e.g. Git) to track changes. Include a README describing how to run each script.
* **Environment Records:** Document software and package versions (e.g. via `sessionInfo()` or `pip freeze`). This is critical for reproducibility.
* **Code Comments:** Write clear comments explaining non-obvious logic (e.g. filtering rules, unusual data issues). Each exported CSV should be generated by a specific script or function, with provenance noted in code.
* **Logging:** Where appropriate, have scripts write logs of their actions (e.g. number of records cleaned, any exceptions). This supports auditing and troubleshooting.
* **Peer Review:** Before finalizing, have analysis scripts and results reviewed by an independent analyst and a domain expert (microbiologist or epidemiologist) to ensure accuracy and clarity.

## Outputs and File Management

* **CSV Outputs:** For each major analysis section (e.g. “Isolate\_Counts”, “Resistance\_Summary”, “Time\_Trends”), export the final tables as CSV named `AMR_Analysis_<SectionName>.csv` into `data/processed/Tables`. Ensure each CSV has a header row with clear column names and a brief description (e.g. in a README or in a separate metadata file). These CSVs should be immediately usable for report writing or further analysis.
* **Clean Data:** The exported CSVs must be free of row indices, comments, or formatting artifacts. All data fields should be atomic (no embedded newlines or delimiter characters). Missing values should be consistently marked (e.g. blank or NA).
* **Summary Materials:** Include in the outputs any summary tables or figures that will go directly into the national report. For example, export a table of WHO priority pathogen resistance rates or an image file of a key chart. Document the rationale for each included output so report writers can contextualize them.

## Stakeholder Interpretation and Reporting

* **Focus on Policy-Relevant Findings:** Highlight trends and results that matter to public health authorities. For example, rising resistance in a key pathogen may prompt updates to treatment guidelines. Provide commentary (in code notebooks or comments) linking findings to policy questions.
* **One Health Perspective:** Although this data is human-focused, mention any implications for animal or environmental sectors (e.g. if a One Health pathogen shows unusual trends). Frame results in the context of Ghana’s AMR National Action Plan and One Health objectives.
* **Confidence and Caveats:** Clearly note limitations (e.g. if data are from sentinel sites only, or if missing data may bias results). Use WHO/GLASS language where possible to describe confidence in surveillance data and known biases.
* **Clarity for Non-technical Audiences:** When summarizing results (for example, in report tables), use plain language and define any technical terms. For each figure/table, prepare a brief interpretation (e.g. “X% of *E. coli* in 2023 were ESBL producers, significantly higher than 2019” or “MRSA prevalence remains low”).

**Sources:** Guidance is drawn from international AMR surveillance standards and literature. For example, WHO emphasizes standardized methods and de-duplication in national AMR surveillance, and CLSI M39 stresses that data must be reliably collected and analyzed to be useful. We also follow WHO’s priority pathogen lists and One Health principles to ensure the analysis is globally relevant and locally actionable. These standards will ensure consistency, scientific rigor, and policy relevance in the Ghana One Health AMR report.

## Final Notes
