
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

Font:
we are going to be using 2 fonts.

Font names : 

Cormorant Garamond : Used mostly for names and titles. 
Montserrat: was mostly used for descriptions. 

- when pressing a certain text you could see it's font at the typography section in figma
- use this article to understand the fonts propreties ( https://developer.mozilla.org/en-US/docs/Web/CSS/font-weight)


imports ( add it to the head of your html) : 
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">


how to use for a certain object (body , text , paragraph , class  etc.... ):
h1, h2, h3, h4 {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 600;
}

Preventing Css overlapping: 

1. Use Scoped Styling with CSS Classes
use unique class names or IDs for their styles. Avoid targeting generic tags like p, h1, or div directly. For example:

<!-- Instead of styling all p tags -->
<p class="section1-paragraph">This is specific to section 1</p>

<!-- CSS -->
.section1-paragraph {
    color: blue;
    font-size: 16px;
}

This ensures their styles apply only to their specific section.


2. Use Namespaced CSS
wrap your section in a unique container or parent class to create a namespace. This isolates their styles within their section.

<div class="section1">
    <p>This is section 1</p>
</div>

<div class="section2">
    <p>This is section 2</p>
</div>


.section1 p {
    color: red;
}

.section2 p {
    color: green;
}


5. Scope Styles Using id for Each Section
If you prefer inline scoping without heavy use of classes, use id selectors.


<div id="section1">
    <p>This is a paragraph in section 1</p>
</div>

<div id="section2">
    <p>This is a paragraph in section 2</p>
</div>


#section1 p {
    font-size: 14px;
}

#section2 p {
    font-size: 16px;
}


8. Clear Team Guidelines
Document styling rules for the team:

No global styles.
All styles must use unique class names or be scoped to specific containers.
Use comments for clarity where necessary.

<!-- This is the best way of doing it -->

9. Use Unique Class Prefixes for Each Contributor's Section
Assign a unique class prefix or namespace to each of your sections. This ensures that your styles are scoped to your specific section.

Example:


<section id="product1" class="products-section products-section-1">
    <div class="product-info product-info-1">Product info for section 1</div>
</section>

<section id="product2" class="products-section products-section-2">
    <div class="product-info product-info-2">Product info for section 2</div>
</section>


/* Styles for Section 1 */
.products-section-1 .product-info {
    color: red;
    background-color: lightgray;
}

/* Styles for Section 2 */
.products-section-2 .product-info {
    color: blue;
    background-color: white;
}
This ensures that even though the structure is similar, each section has unique styles.

<!-- A better approach of doing it -->

10. Use a Parent Container for Each Section
Wrap each section in a parent container with a unique id or class to scope all child elements.

Example:

<div id="section1-container">
    <section id="product1" class="products-section">
        <div class="product-info">Product info for section 1</div>
    </section>
</div>

<div id="section2-container">
    <section id="product2" class="products-section">
        <div class="product-info">Product info for section 2</div>
    </section>
</div>


/* Scoped styles for Section 1 */
#section1-container .products-section .product-info {
    font-size: 18px;
    color: green;
}

/* Scoped styles for Section 2 */
#section2-container .products-section .product-info {
    font-size: 20px;
    color: orange;
}





