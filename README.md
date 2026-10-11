dataset col description 
**Resume_str**
Most useful to start

This contains the resume as readable text, including sections such as:
- Professional summary
- Skills
- Work experience
- Education
- Accomplishments
Example: You can give this text to an AI model and ask it to extract the candidate's skills, years of experience, education, and previous roles.


**Resume_html**
This contains the resume in HTML format — code that describes the document's structure and formatting.
For example, it may contain tags such as <div>, <span>, and attributes describing sections and layout.
What is it for? It can help you experiment with extracting text from structured HTML. You can ignore it for your first experiments because Resume_str already contains readable text.


**Category**
This tells you the resume's occupational category.
Examples include HR, INFORMATION-TECHNOLOGY, ACCOUNTANT, and ENGINEERING.
What is it for? It provides a label if you want to build a model that predicts a resume's professional category. It does not tell you whether the resume is good or bad, and it is not a job description.