PROMPT_SYSTEM = '''
                You will analyze a research article for adherence to specific criteria. For each question, answer with "True" if the criterion is met, "False" if it is not, and "N/A" if the criterion is not applicable to the article. Use the specified output format to ensure consistency.
                For questions related to NHST (i.e., Category B), consider whether statistical testing is appropriate for the study (e.g., performance evaluation). If NHST is not performed (B2), mark the criterion as "False" and mark all the remaining Category B questions as "N/A".
                '''

PROMPT_USER = '''
              CHECKLIST TO EVALUATE
     
              CATEGORY A: Descriptive and Methodological Criteria
     
                  A1. Is the parameter setting methodology documented?
                  A2. Are the performance metrics clearly defined?
                  A3. Is a measure of central tendency provided for the chosen performance metrics?
                  A4. Is a measure of variability provided for the chosen performance metrics?
                  A5. Is a measure of symmetry provided for the chosen performance metrics?
                  A6. Is a measure of tailedness provided for the chosen performance metrics?
                  A7. Are confidence intervals provided for the chosen performance metrics?
                  A8. Are the performance metrics distributions plotted?
                  A9. Are sample sizes adequate (≥30)?
                  A10. Are sample sizes equal?
                  A11. Is computation effort discussed?
                  A12. Is the source code freely available?
                  A13. Are the limitations of the study discussed?
     
              CATEGORY B: Null Hypothesis Statistical Testing (NHST) Criteria
     
                  B1. Could NHST have been performed?
                  B2. Is NHST performed?
                  B3. Is power analysis done a priori?
                  B4. Are the test assumptions discussed and/or verified?
                  B5. Is the significance level (α) provided?
                  B6. Is the familywise Type I error rate controlled?
                  B7. Are exact test statistics provided?
                  B8. Are exact p-values provided?
                  B9. Are statistically non-significant results discussed?
                  B10. Are effect sizes provided?
     
              EXPECTED OUTPUT FORMAT
     
              You shall provide your answer in the following format without additional commentary :
              
              {
                 "Category A": {
                     "A1": "True/False/N/A",
                     "A2": "True/False/N/A",
                     "A3": "True/False/N/A",
                     "A4": "True/False/N/A",
                     "A5": "True/False/N/A",
                     "A6": "True/False/N/A",
                     "A7": "True/False/N/A",
                     "A8": "True/False/N/A",
                     "A9": "True/False/N/A",
                     "A10": "True/False/N/A",
                     "A11": "True/False/N/A",
                     "A12": "True/False/N/A",
                     "A13": "True/False/N/A"
              },
                 "Category B": {
                     "B1": "True/False/N/A",
                     "B2": "True/False/N/A",
                     "B3": "True/False/N/A",
                     "B4": "True/False/N/A",
                     "B5": "True/False/N/A",
                     "B6": "True/False/N/A",
                     "B7": "True/False/N/A",
                     "B8": "True/False/N/A",
                     "B9": "True/False/N/A",
                     "B10": "True/False/N/A"
                 }
              }
              '''
