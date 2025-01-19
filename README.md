
Project Instructions for Website Development
Overview
Each team member will select a section from the homepage to work on. Follow the steps below to ensure clarity and successful completion of your tasks.

Steps to Follow
Copy the Header:

Start by copying the header from main_page.html.
Create Your Files:

Create your working files in the folder designated with your name.
Access Figma Project:

The website design has already been completed. You can access the design through the Figma project link available in the "Links" tab in the Discord file or the Notion project file:
Notion Project File.
Resource Table:

Add a resources table that allows you to:
Save or add your own resources.
Access video resources or Arctica's resource page.
Reformatting Descriptions:

If you’re responsible for reformatting descriptions across the entire site:
Copy the entire design layout.
Add a third page, paste the design, and make necessary changes while ensuring that your work does not appear AI-generated (use your creativity to enhance the existing structure).
Important Notes:
Identify Your Contributions:
When submitting your work, clearly add your name and specify the section you are working on.
Example:
ANAS: Product section and header.



Color Palette
What's Included:
To maintain a consistent design throughout the website, the following color palette should be defined in your CSS. Paste this code at the top of your CSS file:

:root {
    --color-primary: #2c4a3c;
    --color-secondary: #94a18d;
    --color-accent: #c69455;
    --color-background: #fcf9f2;
    --color-text: #1a2e28;
    --shadow-soft: 0 10px 30px rgba(0, 0, 0, 0.08);
    --shadow-strong: 0 15px 40px rgba(0, 0, 0, 0.12);
    --footer-background: #1a2e28;
}

How to Use the Color Palette:

Accessing Colors:

Use the variables defined in the :root selector by referencing them with the var() function. For example, to set a background color, you could use:

body {
    background-color: var(--color-background);
}

(check the figma design for the hex code in the fill section you could see the hex code for each object ) 



