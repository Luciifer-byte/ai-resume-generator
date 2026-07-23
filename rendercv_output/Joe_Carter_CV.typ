// Import the rendercv function and all the refactored components
#import "@preview/rendercv:0.3.0": *

// Apply the rendercv template with custom configuration
#show: rendercv.with(
  name: "Joe Carter",
  title: "Joe Carter - CV",
  footer: context { [#emph[Joe Carter -- #str(here().page())\/#str(counter(page).final().first())]] },
  top-note: [ #emph[Last updated in July 2026] ],
  locale-catalog-language: "en",
  text-direction: ltr,
  page-size: "a4",
  page-top-margin: 0.6in,
  page-bottom-margin: 0.6in,
  page-left-margin: 0.3in,
  page-right-margin: 0.3in,
  page-show-footer: false,
  page-show-top-note: false,
  colors-body: rgb(0, 0, 0),
  colors-name: rgb(8, 89, 28),
  colors-headline: rgb(0, 0, 0),
  colors-connections: rgb(0, 95, 115),
  colors-section-titles: rgb(8, 89, 28),
  colors-links: rgb(0, 56, 69),
  colors-footer: rgb(128, 128, 128),
  colors-top-note: rgb(128, 128, 128),
  typography-line-spacing: 0.6em,
  typography-alignment: "justified",
  typography-date-and-location-column-alignment: right,
  typography-font-family-body: "Charter",
  typography-font-family-name: "Helvetica",
  typography-font-family-headline: "Helvetica",
  typography-font-family-connections: "Helvetica",
  typography-font-family-section-titles: "Helvetica",
  typography-font-size-body: 12pt,
  typography-font-size-name: 24pt,
  typography-font-size-headline: 12pt,
  typography-font-size-connections: 12pt,
  typography-font-size-section-titles: 15pt,
  typography-small-caps-name: false,
  typography-small-caps-headline: false,
  typography-small-caps-connections: false,
  typography-small-caps-section-titles: false,
  typography-bold-name: true,
  typography-bold-headline: false,
  typography-bold-connections: false,
  typography-bold-section-titles: true,
  links-underline: true,
  links-show-external-link-icon: false,
  header-alignment: center,
  header-photo-width: 3.5cm,
  header-space-below-name: 0.7cm,
  header-space-below-headline: 0.7cm,
  header-space-below-connections: 0.7cm,
  header-connections-hyperlink: true,
  header-connections-show-icons: false,
  header-connections-display-urls-instead-of-usernames: true,
  header-connections-separator: "•",
  header-connections-space-between-connections: 0.5cm,
  section-titles-type: "with_full_line",
  section-titles-line-thickness: 0.5pt,
  section-titles-space-above: 0.9cm,
  section-titles-space-below: 0.3cm,
  sections-allow-page-break: true,
  sections-space-between-text-based-entries: 0.3em,
  sections-space-between-regular-entries: 0.9em,
  entries-date-and-location-width: 3.5cm,
  entries-side-space: 0.2cm,
  entries-space-between-columns: 0.1cm,
  entries-allow-page-break: false,
  entries-short-second-row: false,
  entries-degree-width: 1cm,
  entries-summary-space-left: 0cm,
  entries-summary-space-above: 0cm,
  entries-highlights-bullet:  "◦" ,
  entries-highlights-nested-bullet:  "◦" ,
  entries-highlights-space-left: 0.9cm,
  entries-highlights-space-above: 0cm,
  entries-highlights-space-between-items: 0.1cm,
  entries-highlights-space-between-bullet-and-text: 0.5em,
  date: datetime(
    year: 2026,
    month: 7,
    day: 23,
  ),
)


= Joe Carter

#connections(
  [San Francisco, California, USA],
  [#link("mailto:alex.carter@example.com", icon: false, if-underline: false, if-color: false)[alex.carter\@example.com]],
  [#link("tel:+1-415-555-0189", icon: false, if-underline: false, if-color: false)[(415) 555-0189]],
  [#link("https://linkedin.com/in/alex-carter-marketing", icon: false, if-underline: false, if-color: false)[linkedin.com\/in\/alex-carter-marketing]],
  [#link("https://github.com/alexcarterdev", icon: false, if-underline: false, if-color: false)[github.com\/alexcarterdev]],
)


== Summary

Marketing professional with 7+ years of experience in growth marketing, brand strategy, digital campaigns, and analytics. Experienced in leading cross-functional initiatives, optimizing customer acquisition, and using AI-assisted workflows to improve marketing efficiency.


== Skills

#strong[Marketing:] Brand Strategy, Growth Marketing, Product Marketing, Campaign Management

#strong[Analytics:] Google Analytics 4, Tableau, Power BI, Looker Studio

#strong[Digital:] Google Ads, Meta Ads, LinkedIn Ads, SEO, Email Marketing

#strong[Tools:] HubSpot, Salesforce, Canva, Figma, Notion, Microsoft 365

#strong[Languages:] English (Native), Spanish (Professional)

== Professional Experience

#regular-entry(
  [
    #strong[Senior Marketing Manager]

    #emph[Netflix]

  ],
  [
    #emph[Los Angeles, California]

    #emph[Jan 2022 – present]

  ],
  main-column-second-row: [
    - Led integrated marketing campaigns reaching 50M+ users.

    - Increased customer acquisition by 28\% through data-driven optimization.

    - Managed \$5M annual digital advertising budget.

  ],
)

#regular-entry(
  [
    #strong[Digital Marketing Specialist]

    #emph[HubSpot]

  ],
  [
    #emph[Boston, Massachusetts]

    #emph[June 2019 – Dec 2021]

  ],
  main-column-second-row: [
    - Increased organic traffic by 70\% through SEO initiatives.

    - Built automated email campaigns improving lead conversion by 40\%.

  ],
)

#regular-entry(
  [
    #strong[Marketing Coordinator]

    #emph[Adobe]

  ],
  [
    #emph[San Jose, California]

    #emph[July 2017 – May 2019]

  ],
  main-column-second-row: [
    - Supported product launch campaigns across North America.

    - Coordinated influencer and social media marketing initiatives.

  ],
)

== Education

#education-entry(
  [
    #strong[University of Southern California]

    #emph[Bachelor of Business Administration] #emph[in] #emph[Marketing]

  ],
  [
    #emph[Los Angeles, California]

    #emph[2013 – 2017]

  ],
  main-column-second-row: [
    - Focus on Digital Marketing, Consumer Behavior, Marketing Analytics.

  ],
)
