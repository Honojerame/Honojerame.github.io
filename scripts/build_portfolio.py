#!/usr/bin/env python3
"""Generate dependency-free GitHub Pages HTML. Run: python3 scripts/build_portfolio.py."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://honojerame.github.io'
GITHUB = 'https://github.com/Honojerame'
LINKEDIN = 'https://www.linkedin.com/in/precious-onojerame-880498183/'
RESUME = "PRESH'S%20RESUME.pdf"
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'


def external(url, label, css='text-link'):
    return f'<a class="{css}" href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{label}{ARROW}<span class="visually-hidden"> (opens in a new tab)</span></a>'


def head(title, description, route):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0b100e">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="author" content="Precious Onojerame">
  <title>{escape(title)}</title>
  <link rel="canonical" href="{ORIGIN}/{route}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title, quote=True)}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{ORIGIN}/{route}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{escape(title, quote=True)}">
  <meta name="twitter:description" content="{escape(description, quote=True)}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="favicon.png" sizes="any">
  <link rel="preload" href="fonts/poppins-regular-webfont.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/portfolio.css">
  <script src="assets/portfolio.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>'''


def header(home=False):
    prefix = '' if home else 'index.html'
    work = '#work' if home else 'projects.html'
    current = '' if home else ' aria-current="true"'
    return f'''<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Precious Onojerame, home"><span class="monogram" aria-hidden="true">PO</span><span class="brand-name">Precious Onojerame<span class="brand-period accent">.</span></span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-navigation" hidden>Menu +</button>
    <nav class="site-nav" id="site-navigation" aria-label="Main navigation">
      <a href="{work}"{current}>Work</a><a href="{prefix}#about">About</a><a href="{prefix}#experience">Experience</a><a href="{prefix}#contact">Contact</a>
      {external(GITHUB, 'GitHub', 'nav-outbound')}
    </nav>
  </div>
</header>'''


def footer():
    return '''<footer class="site-footer"><div class="container footer-inner">
  <span>© <span data-year>2026</span> Precious Onojerame</span>
  <div class="footer-secondary"><a href="https://twitter.com/Honojerame" target="_blank" rel="noopener noreferrer">X / Twitter ↗</a><a href="https://www.facebook.com/profile.php?id=100074418820867" target="_blank" rel="noopener noreferrer">Facebook ↗</a><a href="#main">Back to top ↑</a></div>
</div></footer>
</body>
</html>'''


def tags(items):
    return '<div class="tags">' + ''.join(f'<span class="tag">{escape(s)}</span>' for s in items) + '</div>'


def circuit():
    # A conceptual embedded-system diagram: input, processing, memory,
    # output, and telemetry. Traces encode those relationships.
    pins = ''.join(f'<path class="wire" d="M{x} 195v20 M{x} 365v20"/>' for x in range(219, 333, 14))
    pins += ''.join(f'<path class="wire" d="M181 {y}h24 M355 {y}h24"/>' for y in range(230, 355, 14))
    return f'''<figure class="hero-figure">
<svg class="schematic" viewBox="0 0 560 530" role="img" aria-labelledby="system-title system-desc">
 <title id="system-title">Intelligent embedded systems</title>
 <desc id="system-desc">A conceptual system diagram: sensors feed a compute core, which exchanges data with memory, controls actuators, and sends telemetry to software.</desc>
 <defs><pattern id="board-grid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".75" fill="#2a3e2f"/></pattern></defs>
 <rect x="20" y="24" width="520" height="476" fill="url(#board-grid)"/>
 <path class="wire" d="M50 120V77h135l25-25h280v120l26 26v230h-86l-25 25H68v-93l-25-25V168l28-28h83l30 30h68 M57 402h97l45 45h141l20 20h117 M90 58v37h74l25 25h45 M478 81v102l-55 55 M88 470v-44 M512 374h-57l-25 25h-73"/>
 <path class="wire" d="M276 136v34l-15 15v30 M295 136v43l-20 20v16 M138 248h31l36 24 M138 266h29l38 34 M355 244h29l30-30h50 M355 258h39l30-30h40 M355 322h27l40 40v76 M355 336h21l31 31v71 M249 365v53l-29 29h-75 M233 365v39l-29 29h-59"/>
 <path class="active-wire" d="M138 257h26l41 29 M284 136v40l-16 16v23 M355 251h35l30-30h44 M355 329h24l36 36v73"/>
 <path class="signal" d="M138 257h26l41 29 M355 251h35l30-30h44"/>
 {pins}
 <rect class="module" x="46" y="230" width="92" height="54" rx="3"/><text x="92" y="253" text-anchor="middle">SENSORS</text><text class="small" x="92" y="270" text-anchor="middle">INPUT</text>
 <rect class="module" x="233" y="82" width="102" height="54" rx="3"/><text x="284" y="105" text-anchor="middle">MEMORY</text><text class="small" x="284" y="122" text-anchor="middle">DATA</text>
 <rect class="module" x="429" y="191" width="95" height="58" rx="3"/><text x="476" y="216" text-anchor="middle">ACTUATORS</text><text class="small" x="476" y="234" text-anchor="middle">OUTPUT</text>
 <rect class="module" x="365" y="414" width="103" height="56" rx="3"/><text x="417" y="438" text-anchor="middle">SOFTWARE</text><text class="small" x="417" y="456" text-anchor="middle">TELEMETRY</text>
 <rect class="core" x="205" y="215" width="150" height="150" rx="4"/><rect x="216" y="226" width="128" height="128" rx="1" fill="none" stroke="#375233"/>
 <circle cx="226" cy="236" r="3" fill="#bdff83"/><text class="small" x="280" y="261" text-anchor="middle">HW × SW</text><text class="core-title" x="280" y="296" text-anchor="middle">COMPUTE</text><text class="small" x="280" y="323" text-anchor="middle">CONTROL + AI</text>
 <text class="small" x="211" y="398">U1 / PROCESSING</text><text class="small" x="47" y="310">J1</text><text class="small" x="429" y="274">J2</text>
 <circle class="live-pin" cx="145" cy="447" r="4"/><circle class="pin" cx="145" cy="433" r="4"/>
 <circle class="pin" cx="57" cy="402" r="4"/><circle class="pin" cx="88" cy="470" r="4"/><circle class="pin" cx="90" cy="58" r="4"/><circle class="pin" cx="478" cy="81" r="4"/>
 <circle class="pin" cx="50" cy="48" r="7"/><circle class="pin" cx="510" cy="48" r="7"/><circle class="pin" cx="50" cy="477" r="7"/><circle class="pin" cx="510" cy="477" r="7"/>
</svg><figcaption><span>CONCEPT / EMBEDDED SYSTEM</span><span>INPUT → COMPUTE → OUTPUT</span></figcaption>
</figure>'''


def visual(kind, uid, accessible=False):
    drawings = {
      'amhs': '''<text class="svg-small" x="22" y="25">CONTROL ARCHITECTURE</text><path d="M88 74H430M88 82H430 M126 82v29 M384 82v29"/><rect x="93" y="110" width="67" height="44" rx="3"/><text x="126" y="137" text-anchor="middle">FOUP</text><rect x="351" y="110" width="67" height="44" rx="3"/><text x="384" y="137" text-anchor="middle">FOUP</text><rect x="197" y="51" width="118" height="52" rx="4"/><text class="svg-title" x="256" y="75" text-anchor="middle">OHT</text><text class="svg-small" x="256" y="91" text-anchor="middle">SERVO + HOIST</text><path d="M256 103v55 M162 132h35 M315 132h34 M197 132v26h118v-26"/><text class="svg-accent" x="256" y="182" text-anchor="middle">FSM · INTERLOCKS · TELEMETRY</text><circle cx="88" cy="78" r="4"/><circle cx="430" cy="78" r="4"/>''',
      'prisca': '''<text class="svg-small" x="22" y="25">FORECASTING PIPELINE</text><rect x="28" y="54" width="127" height="42" rx="3"/><text x="91" y="79" text-anchor="middle">PRICE HISTORY</text><rect x="28" y="118" width="127" height="42" rx="3"/><text x="91" y="143" text-anchor="middle">NEWS SENTIMENT</text><path d="M155 75h27l25 25h20 M155 139h27l25-25h20"/><rect x="227" y="80" width="107" height="53" rx="4"/><text class="svg-title" x="280" y="112" text-anchor="middle">XGBoost</text><path d="M334 106h35l24-24h50 M393 82l-6-1m6 1l-1 6"/><text class="svg-accent" x="407" y="116" text-anchor="middle">NEXT OPEN</text><text class="svg-small" x="22" y="186">PRISCA / MACHINE LEARNING + NLP</text>''',
      'solar': '''<text class="svg-small" x="22" y="25">SOLAR ENERGY FORECASTING</text><rect x="30" y="73" width="119" height="54" rx="3"/><text x="89" y="96" text-anchor="middle">WEATHER</text><text class="svg-small" x="89" y="113" text-anchor="middle">+ ENERGY DATA</text><path d="M149 100h40"/><rect x="189" y="67" width="124" height="66" rx="4"/><text class="svg-title" x="251" y="105" text-anchor="middle">LightGBM</text><path d="M313 100h40"/><rect x="353" y="73" width="118" height="54" rx="3"/><text x="412" y="96" text-anchor="middle">POWER</text><text class="svg-small" x="412" y="113" text-anchor="middle">FORECAST</text><text class="svg-accent" x="251" y="174" text-anchor="middle">FEATURES → MODELS → EVALUATION</text>''',
      'bus': '''<text class="svg-small" x="22" y="25">OBJECT-ORIENTED SYSTEM</text><rect x="183" y="52" width="136" height="48" rx="3"/><text class="svg-title" x="251" y="82" text-anchor="middle">Ticketing</text><path d="M251 100v23H87v22 M251 123v22 M251 123h164v22"/><rect x="32" y="145" width="110" height="37" rx="3"/><rect x="196" y="145" width="110" height="37" rx="3"/><rect x="360" y="145" width="110" height="37" rx="3"/><text x="87" y="168" text-anchor="middle">ADMIN</text><text x="251" y="168" text-anchor="middle">DRIVER</text><text x="415" y="168" text-anchor="middle">PASSENGER</text>''',
      'sentiment': '''<text class="svg-small" x="22" y="25">BOOK REVIEW CLASSIFICATION</text><rect x="24" y="77" width="116" height="55" rx="3"/><text x="82" y="101" text-anchor="middle">REVIEW</text><text class="svg-small" x="82" y="119" text-anchor="middle">TEXT INPUT</text><path d="M140 104h34l33-44h33 M174 104l33 44h33"/><rect x="240" y="39" width="145" height="44" rx="3"/><text x="312" y="65" text-anchor="middle">TF–IDF + LOGREG</text><rect x="240" y="127" width="145" height="44" rx="3"/><text x="312" y="154" text-anchor="middle">BiLSTM</text><path d="M385 61h27l33 43-33 44h-27"/><circle cx="445" cy="104" r="5"/><text class="svg-small" x="23" y="187">BASELINE / NEURAL MODEL COMPARISON</text>''',
      'web': '''<text class="svg-small" x="22" y="25">BROWSER APPLICATION</text><rect x="75" y="48" width="350" height="121" rx="4"/><path d="M75 74h350"/><circle cx="92" cy="61" r="3"/><circle cx="105" cy="61" r="3"/><circle cx="118" cy="61" r="3"/><text class="svg-title" x="250" y="114" text-anchor="middle">INPUT → LOGIC → UI</text><text class="svg-small" x="250" y="142" text-anchor="middle">JAVASCRIPT / HTML / CSS</text>'''
    }
    descriptions = {
      'amhs': 'AMHS controls concept: FOUP carriers, overhead hoist transport, servo and hoist control, and state-machine interlocks.',
      'prisca': 'Historical prices and news sentiment feed an XGBoost model to forecast the next SPY opening price.',
      'solar': 'Weather and energy data feed a LightGBM model to forecast solar power.',
      'bus': 'Ticketing workflows connect administrator, driver, and passenger roles.',
      'sentiment': 'Book review text is classified using a TF-IDF logistic regression baseline and a bidirectional LSTM.',
      'web': 'A browser application connects user input, JavaScript logic, and the interface.'
    }
    attrs = f'role="img" aria-labelledby="{uid}-title"' if accessible else 'aria-hidden="true"'
    title = f'<title id="{uid}-title">{descriptions[kind]}</title>' if accessible else ''
    return f'<div class="project-visual"><svg class="project-svg" viewBox="0 0 500 210" {attrs}>{title}{drawings[kind]}</svg></div>'


PROJECTS = [
 dict(slug='amhs', title='AMHS FOUP Digital Twin', category='Embedded controls / simulation', kind='amhs', repo=GITHUB+'/amhs-foup-digital-twin', year='2026', role='Independent project', context='Semiconductor manufacturing', stack=['Python','Embedded controls','JavaScript','HMI','CI/CD'], description='A semiconductor-fab digital twin connecting transport scheduling, servo motion, safety interlocks, and a live browser control room.', overview='How do software decisions become safe, coordinated physical motion? I built a digital twin of an automated material handling system (AMHS) to explore that question through the movement of 300 mm wafer carriers, known as FOUPs, inside a simulated semiconductor fab.', approach='A deterministic state machine coordinates overhead hoist transport (OHT), from pickup to delivery. The model connects dispatch logic to acceleration-limited servo motion, position feedback, timed hoist transfers, and emergency-stop recovery.', contributions=['Modeled multi-vehicle transport, FIFO dispatch, and pickup/drop-off sequencing in typed Python.','Connected a proportional position-to-velocity controller with acceleration limits and target-crossing detection.','Built a browser control room with vehicle animation, telemetry, time controls, pause/reset, and fault injection.','Added automated tests, GitHub Actions CI, and system architecture documentation.'], takeaway='The project makes control boundaries visible: scheduling requests, controller states, plant motion, sensor feedback, and the operator interface can be inspected together.', note='This is an independent simulation. Collision avoidance, rail-segment reservations, and a hardware firmware implementation remain roadmap items.'),
 dict(slug='prisca-spy-predictor',title='PRISCA SPY Predictor',category='Machine learning / NLP',kind='prisca',repo=GITHUB+'/prisca-spy-predictor',year='2025',role='ML development & team leadership',context='Break Through Tech AI Studio',stack=['Python','XGBoost','FinBERT','FastAPI','SHAP'],description='A collaborative forecasting pipeline combining historical market data and financial-news sentiment to predict the next SPY opening price.',overview='PRISCA explores whether financial-news sentiment adds useful information to a next-day SPY opening-price forecast. Developed with a six-person AI Studio team, the project combines a price-data pipeline, NLP features, regression models, and a web interface.',approach='Historical price features and news sentiment from VADER and FinBERT feed tree-based regression models. Model comparison and SHAP analysis help the team understand which inputs contribute to the forecast.',contributions=['Contributed machine learning development, model training, and optimization.','Helped coordinate the team as my role evolved from project management to technical leadership.','Worked on feature preparation and evaluation alongside teammates responsible for sentiment analysis, data processing, and the application.'],takeaway='The project reinforced the value of strong baselines and interpretable evaluation. Prior-price features were more influential than sentiment in the documented experiments.',note='A collaborative educational forecasting project. Reported historical model metrics are not evidence of live trading performance.'),
 dict(slug='solar',title='Solar Power Forecasting',category='Applied AI / research',kind='solar',repo=GITHUB+'/AI-Solar_Power_Prediciton',year='Undergraduate research',role='Research & model development',context='Eastern New Mexico University',stack=['Python','LightGBM','scikit-learn','pandas'],description='Machine learning research that turns historical weather and energy data into solar-generation forecasts.',overview='Solar generation changes with weather conditions. This undergraduate research project investigates how historical energy and meteorological features can support useful power-output forecasts.',approach='I worked through the complete modeling pipeline: cleaning and preparing data, exploring relationships, engineering features, comparing regression models, and tuning hyperparameters.',contributions=['Compared LightGBM, ExtraTrees, and Ridge regression models.','Evaluated predictions using MAE, RMSE, and R².','Examined how weather variables, including solar radiation and temperature, relate to generation.','Presented the research at a student research conference.'],takeaway='The work connects machine learning with an energy-system problem, emphasizing evaluation and interpretation alongside predictive performance.',note='Research results depend on the dataset and evaluation setup. The repository contains the analysis and modeling workflow.'),
 dict(slug='bus-ticket',title='Bus Ticket Management',category='Software engineering / Java',kind='bus',repo=GITHUB+'/CS234_BusTicketManagementSystem',year='Spring 2025',role='Developer & Scrum Master',context='ENMU / collaborative course project',stack=['Java','Swing','OOP','File I/O','Scrum'],description='A Java desktop application for bus, driver, passenger, and ticket-management workflows, built with a student team.',overview='This semester-long team project brings transport administration and passenger booking into one Java Swing application. Separate user roles organize the workflows for administrators, drivers, and passengers.',approach='Object-oriented design separates responsibilities across the application. Swing provides the desktop interface, while file I/O supports persistent records.',contributions=['Designed and implemented Admin, Driver, and Passenger classes.','Built the TicketHistoryGUI and integrated file handling and login logic.','Served as Scrum Master during the project and supported team coordination.','Contributed to the project recognized as Best Project in CS234, Spring 2025.'],takeaway='Working across class design, interface logic, persistence, and team delivery helped me connect software architecture with the needs of actual users.',note='A collaborative academic application built for a fictional transit company.'),
 dict(slug='ecornell',title='Book Review Sentiment Classifier',category='Machine learning / NLP',kind='sentiment',repo=GITHUB+'/eCornell_Final_Project',year='2025',role='Model development & evaluation',context='Machine Learning Foundations',stack=['Python','TF–IDF','Logistic regression','BiLSTM'],description='A direct comparison of a TF–IDF logistic-regression baseline and a bidirectional LSTM for classifying book-review sentiment.',overview='I built two models to classify Amazon book reviews as positive or negative, using the same dataset to compare a simpler text-classification baseline with a neural approach.',approach='The baseline represents text with TF–IDF and classifies it with logistic regression. The neural model tokenizes and pads sequences, then applies an embedding layer, a bidirectional LSTM, and a sigmoid output.',contributions=['Implemented and evaluated both approaches on book-review text.','Compared test accuracy instead of assuming the neural model would perform better.','Identified pretrained embeddings and regularization as potential areas for further experimentation.'],takeaway='The baseline reached 80% test accuracy, while the initial LSTM with random embeddings reached 74.5%. The simpler model performed better in this experiment.',note='These are the test results reported in the project repository; proposed improvements have not been presented as achieved results.'),
 dict(slug='pacmen',title='PacMen',category='JavaScript / interaction',kind='web',repo=GITHUB+'/PacMen-exercise',demo='https://honojerame.github.io/PacMen-exercise',year='2022',role='Developer',context='MIT xPRO exercise',stack=['JavaScript','HTML','CSS','DOM'],description='An interactive browser exercise that creates moving PacMan characters and keeps them inside the screen boundaries.',overview='A hands-on exploration of browser animation, DOM manipulation, and boundary detection. Visitors can add characters and start their movement.',approach='JavaScript updates each character’s position and reverses its direction when it reaches the edge of the available space.',contributions=['Created characters dynamically through button interactions.','Implemented position updates and edge-detection logic.'],takeaway='A foundational exercise in making JavaScript state visible through an interactive interface.',note='An early learning project, retained as part of my software-development journey.'),
 dict(slug='eyes',title='Eyes',category='JavaScript / interaction',kind='web',repo=GITHUB+'/EYES-PROJECT',demo='https://honojerame.github.io/EYES-PROJECT/',year='2022',role='Developer',context='MIT xPRO exercise',stack=['JavaScript','HTML','CSS','DOM'],description='A browser interaction in which a pair of eyes follows the cursor using pointer coordinates and DOM updates.',overview='This small interaction explores the relationship between pointer input and visual feedback. The eyes follow the cursor as it moves around the screen.',approach='An event listener reads the mouse position and maps its coordinates to the positions of the pupils.',contributions=['Connected mouse-move events to element positioning.','Used JavaScript and CSS to translate input coordinates into a visual response.'],takeaway='A focused exercise in event handling, coordinates, and direct DOM manipulation.',note='The original mouse-driven demo is best experienced on a device with a pointer.'),
 dict(slug='realtimebustracker',title='Real-time Bus Tracker',category='JavaScript / APIs',kind='web',repo=GITHUB+'/Bus-tracker',demo='https://honojerame.github.io/Bus-tracker/',year='2022',role='Developer',context='MIT xPRO exercise',stack=['JavaScript','Transit API','Maps','HTML/CSS'],description='A transit-data exercise that plots bus locations on a map and refreshes their positions periodically.',overview='This project connects an external transit API to a map, turning location data into an interface that shows bus movement in Boston.',approach='The application requests vehicle locations and updates map markers on a ten-second interval.',contributions=['Integrated a transit API with a browser map.','Updated marker positions from refreshed vehicle-location data.'],takeaway='The exercise introduced API consumption, asynchronous updates, and location-based interfaces.',note='The original demo depends on third-party transit and mapping services; their availability may affect its behavior.'),
 dict(slug='movies',title='Movies',category='Collaborative web development',kind='web',repo='https://github.com/leonsuaren/moviesRepo',year='2022',role='Header & footer development',context='MIT xPRO team project',stack=['JavaScript','HTML','CSS','Team development'],description='A collaborative movie-web-project contribution focused on the page header and footer.',overview='An early team project that provided experience contributing to a shared web interface and coordinating changes with other developers.',approach='My contribution focused on the header and footer, giving the application consistent framing and navigation.',contributions=['Implemented the project’s header and footer.','Collaborated within a shared codebase.'],takeaway='The work offered practical experience with ownership boundaries and collaboration in front-end development.',note='An archived learning project. The linked repository contains the team’s work.')
]


def card(p, i):
    return f'''<a class="project-card" href="project-{p['slug']}.html">
 {visual(p['kind'], 'card-'+str(i))}<div class="project-copy">
 <div class="overline">{escape(p['category'])}</div><div class="project-title"><h3>{escape(p['title'])}</h3>{ARROW}</div>
 <p>{escape(p['description'])}</p>{tags(p['stack'][:4])}</div></a>'''


def home():
    content = head('Precious Onojerame | Hardware, Software & Intelligent Systems', 'Aspiring computer engineer and Module Equipment Technician at Intel. Explore projects in embedded controls, digital twins, software, and machine learning.', '') + header(True)
    content += f'''<main id="main">
<span id="page1" class="anchor-alias"></span>
<div class="container">
 <section class="hero" aria-labelledby="hero-title">
  <div class="hero-copy"><p class="eyebrow">HELLO, I'M PRECIOUS ONOJERAME</p>
   <h1 id="hero-title">Where hardware<br>meets<br><span class="accent">intelligence.</span></h1>
   <p class="hero-description"><strong>Aspiring computer engineer.</strong> Building across embedded systems, software, and machine learning, with hands-on semiconductor experience at Intel.</p>
   <div class="actions"><a class="button" href="#work">Explore my work <span class="arrow" aria-hidden="true">↓</span></a><a class="button button-quiet" href="#contact">Let's connect {ARROW}</a></div>
   <p class="hero-footnote">Albuquerque, New Mexico / Curious by design.</p>
  </div>{circuit()}
 </section>
 <div class="hero-facts" aria-label="At a glance">
  <div class="fact"><span class="overline">Currently / Intel</span><p>Module Equipment Technician</p></div>
  <div class="fact"><span class="overline">Studying / ENMU</span><p>Computer Science + Electronics Engineering Technology</p></div>
  <div class="fact"><span class="overline">Building toward</span><p>Intelligent physical systems</p></div>
 </div>
 <section class="section" id="work" aria-labelledby="work-title"><span id="page5" class="anchor-alias"></span>
  <div class="section-heading"><div><span class="section-index">01 / SELECTED WORK</span><h2 id="work-title">Ideas, made tangible.</h2></div><a class="text-link" href="projects.html">All projects {ARROW}</a></div>
  <div class="project-grid">{''.join(card(p, i) for i,p in enumerate(PROJECTS[:4]))}</div>
 </section>
</div>
<section class="section section-surface" id="about" aria-labelledby="about-title"><span id="page4" class="anchor-alias"></span><span id="page2" class="anchor-alias"></span>
 <div class="container about-layout"><div><span class="section-index">02 / ABOUT ME</span><h2 id="about-title">Curious about the<br>whole system.</h2>
  <p class="lead">I'm drawn to the point where code meets the physical world.</p>
  <p>At Intel, I work with semiconductor manufacturing equipment. At Eastern New Mexico University, I'm studying Computer Science and Electronics Engineering Technology. Together, those experiences shape how I think about reliability, control, and the relationship between hardware and software.</p>
  <p>My goal is to become a computer engineer, building a deeper foundation in embedded systems, computer architecture, and the hardware behind intelligent machines.</p>
  <div class="actions"><a class="text-link" href="{RESUME}" download>Download résumé <span class="arrow" aria-hidden="true">↓</span></a>{external('https://www.youtube.com/watch?v=8y2SUVlU3Co','Introduction video')}</div>
 </div><div class="focus-list" aria-label="Technical focus">
  <article class="focus-item"><svg class="focus-icon" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><rect x="8" y="8" width="20" height="20" rx="2"/><rect x="13" y="13" width="10" height="10"/><path d="M13 3v5m10-5v5M13 28v5m10-5v5M3 13h5m-5 10h5m20-10h5m-5 10h5"/></svg><div><h3>Hardware & embedded systems</h3><p>Digital logic, microcontrollers, sensors, actuators, and control systems. Hands-on FPGA work using the Artix-7 Basys3 and Vivado.</p><p class="stack">C / C++ / Arduino / HDL / Vivado</p></div></article>
  <article class="focus-item"><svg class="focus-icon" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="m11 10-8 8 8 8m14-16 8 8-8 8M21 5l-6 26"/></svg><div><h3>Software & systems</h3><p>Applications, simulation, and interfaces that make complex processes easier to run and understand.</p><p class="stack">Python / Java / JavaScript / React / Git</p></div></article>
  <article class="focus-item"><svg class="focus-icon" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><circle cx="7" cy="9" r="3"/><circle cx="7" cy="27" r="3"/><circle cx="19" cy="18" r="4"/><circle cx="30" cy="7" r="3"/><circle cx="30" cy="28" r="3"/><path d="m10 11 6 5m-6 9 6-5m6-5 6-6m-6 12 6 5"/></svg><div><h3>Machine learning & research</h3><p>Predictive modeling for energy and environmental systems, including solar generation and global-LSTM water-level forecasting research.</p><p class="stack">scikit-learn / TensorFlow / LightGBM / NLP</p></div></article>
 </div></div>
</section>
<section class="section container" id="experience" aria-labelledby="experience-title"><span id="page3" class="anchor-alias"></span>
 <div class="section-heading"><div><span class="section-index">03 / THE JOURNEY</span><h2 id="experience-title">Learning. Building. Evolving.</h2></div></div>
 <div class="experience-layout"><div><h3 class="column-heading">Experience</h3>
  <article class="timeline-item"><p class="overline">August 2026 – Present</p><h3>Intel</h3><h4>Module Equipment Technician</h4><p>Preventive maintenance, troubleshooting, repair, and equipment certification in semiconductor manufacturing, with a focus on reliability, root-cause analysis, and safe operation.</p></article>
  <article class="timeline-item"><p class="overline">2026 / Prior role</p><h3>Kelly Services, assigned to Intel</h3><h4>Electronics / Maintenance Technician II</h4><p>Supported fab equipment maintenance and electrical, mechanical, and electromechanical troubleshooting as a contingent technician.</p></article>
  <article class="timeline-item"><p class="overline">2025–2026</p><h3>Break Through Tech AI</h3><h4>AI Fellow & Ambassador / Salesforce AI Studio</h4><p>Collaborated on a six-person machine learning team, growing from project management into technical leadership while developing the PRISCA forecasting project.</p></article>
 </div><div><h3 class="column-heading">Education & foundations</h3>
  <article class="timeline-item"><p class="overline">In progress</p><h3>Eastern New Mexico University</h3><h4>Computer Science & Electronics Engineering Technology</h4><p>Bachelor's studies connecting algorithms, data structures, digital logic, embedded systems, and electronics.</p></article>
  <article class="timeline-item"><p class="overline">August 2025</p><h3>Cornell University</h3><h4>Machine Learning Foundations Certificate</h4><p>Supervised and unsupervised learning, feature engineering, model evaluation, and practical machine learning.</p></article>
  <article class="timeline-item"><p class="overline">December 2021</p><h3>MIT xPRO</h3><h4>Full Stack Software Development Certificate</h4><p>Full-stack application development with MongoDB, Express, React, and Node.js.</p></article>
 </div></div>
</section>
<section class="recognition container" aria-labelledby="recognition-title"><h2 class="visually-hidden" id="recognition-title">Recognition</h2><div class="recognition-grid">
 <article><span class="overline">ENMU / 2026</span><h3>Outstanding Student in Mathematical Sciences</h3><p>University recognition representing the Computer Science department.</p></article>
 <article><span class="overline">WiDS Datathon / 2026</span><h3>Most Improved Model</h3><p>Team recognition for progress in machine learning model performance.</p></article>
 <article><span class="overline">CS234 / Spring 2025</span><h3>Best Project</h3><p>Team award for the Bus Ticket Management System.</p></article>
</div></section>
<section class="quotes-section container" aria-labelledby="quotes-title"><span id="page7" class="anchor-alias"></span><div class="section-heading"><div><span class="section-index">04 / TESTIMONIALS</span><h2 id="quotes-title">From people I've worked with.</h2></div></div><div class="quotes-grid">
 <blockquote><p>“Precious is very ambitious and professional with an amazing work ethic.”</p><cite>David & Elisa</cite></blockquote>
 <blockquote><p>“He is very hard working and willing to learn whatever he needs to attain his goals.”</p><cite>Amanda / London</cite></blockquote>
 <blockquote><p>“He has a great deal of patience and is willing to do whatever it takes to produce excellent results.”</p><cite>Morgan / Brooklyn</cite></blockquote>
 <blockquote><p>“I loved his work, I will use him again.”</p><cite>Frank / Albuquerque</cite></blockquote>
 <blockquote><p>“The best web designer out there. I loved his modern touch and simple design.”</p><cite>Julian / Denver</cite></blockquote>
 <blockquote><p>“I was super impressed with his work. He is a great illustrator.”</p><cite>Wyatt Requa / Dallas</cite></blockquote>
</div></section>
<section class="contact-section" id="contact" aria-labelledby="contact-title"><span id="page8" class="anchor-alias"></span>
 <div class="container contact-layout"><div><span class="section-index">05 / GET IN TOUCH</span><h2 id="contact-title">Good things start<br>with a conversation.</h2><p>Have an engineering opportunity, a research idea, or an interesting system to build? I'd love to hear about it.</p>
  <a class="text-link contact-email" href="mailto:preciousonoj@gmail.com">preciousonoj@gmail.com {ARROW}</a>
  <div class="social-links">{external(LINKEDIN,'LinkedIn','')}{external(GITHUB,'GitHub','')}</div>
  <div class="contact-meta">Albuquerque, New Mexico<br><a href="tel:+15054153123">+1 505-415-3123</a></div>
 </div><form class="contact-form" id="contact-form" action="https://formspree.io/f/myzrqnev" method="POST">
  <div class="form-row"><div class="field"><label for="contact-name">Name</label><input id="contact-name" name="name" autocomplete="name" placeholder="Your name" maxlength="120" required></div><div class="field"><label for="contact-email">Email</label><input id="contact-email" name="email" type="email" autocomplete="email" placeholder="you@example.com" maxlength="254" required></div></div>
  <div class="field"><label for="contact-subject">Subject <span class="muted">(optional)</span></label><input id="contact-subject" name="subject" placeholder="What do you have in mind?" maxlength="200"></div>
  <div class="field"><label for="contact-message">Message</label><textarea id="contact-message" name="message" rows="4" placeholder="Tell me a little about it…" maxlength="5000" required></textarea></div>
  <div class="form-submit"><button class="button" type="submit">Send message {ARROW}</button><p class="form-note">Or reach out directly by email.</p></div>
  <p id="form-status" class="form-status" role="status" aria-live="polite" aria-atomic="true"></p>
 </form></div>
</section>
</main>'''
    return content + footer()


def projects_page():
    content = head('Projects | Precious Onojerame', 'Explore digital twins, embedded controls, machine learning research, and software projects by Precious Onojerame.', 'projects.html') + header()
    content += '''<main id="main"><section class="page-intro"><div class="container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Work</span></nav><p class="eyebrow">PROJECTS / EXPLORATIONS / RESEARCH</p><h1>From code to<br><span class="accent">real-world systems.</span></h1><p class="intro-text">A selection of work across embedded controls, applied machine learning, and software development.</p></div></section><div class="container"><section class="project-collection" aria-labelledby="featured-title"><div class="collection-heading"><h2 id="featured-title">Featured projects</h2><span class="overline">Hardware / Software / AI</span></div><div class="project-grid">'''
    content += ''.join(card(p, i) for i,p in enumerate(PROJECTS[:5]))
    content += '</div></section><section class="project-collection" aria-labelledby="archive-title"><div class="collection-heading"><h2 id="archive-title">Early explorations</h2><p>Where the foundations took shape.</p></div><div class="archive-list">'
    for i,p in enumerate(PROJECTS[5:],6):
        content += f'<a class="archive-link" href="project-{p["slug"]}.html"><span class="archive-number">{i:02}</span><h3>{p["title"]}</h3><p>{escape(p["description"])}</p>{ARROW}</a>'
    content += '</div></section></div></main>'
    return content + footer()


def detail(p, next_project):
    title = p['title']+' | Precious Onojerame'
    content = head(title,p['description'],'project-'+p['slug']+'.html') + header()
    content += f'''<main id="main"><section class="page-intro"><div class="container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="projects.html">Work</a><span aria-hidden="true">/</span><span aria-current="page">{escape(p['title'])}</span></nav><p class="eyebrow">{escape(p['category'])}</p><h1>{escape(p['title'])}</h1><p class="intro-text">{escape(p['description'])}</p></div></section>
<div class="container"><div class="detail-hero">{visual(p['kind'],'detail-'+p['slug'],True)}<p class="diagram-key">PROJECT CONCEPT / {escape(p['category'].upper())}</p>
 <dl class="project-facts"><div><dt>Contribution</dt><dd>{escape(p['role'])}</dd></div><div><dt>Context</dt><dd>{escape(p['context'])}</dd></div><div><dt>Period</dt><dd>{escape(p['year'])}</dd></div></dl></div>
 <div class="detail-layout"><article class="prose"><h2>The idea</h2><p>{escape(p['overview'])}</p><h2>The approach</h2><p>{escape(p['approach'])}</p><h2>My contribution</h2><ul>{''.join('<li>'+escape(x)+'</li>' for x in p['contributions'])}</ul><h2>What I learned</h2><p>{escape(p['takeaway'])}</p>'''
    if p['slug']=='ecornell':
        content += '<table class="data-table"><caption>Test accuracy reported in the project repository</caption><thead><tr><th scope="col">Model</th><th scope="col">Accuracy</th></tr></thead><tbody><tr><th scope="row">TF–IDF + logistic regression</th><td>80%</td></tr><tr><th scope="row">BiLSTM, random embeddings</th><td>74.5%</td></tr></tbody></table>'
    content += f'''</article><aside class="detail-aside" aria-label="Project links and technologies"><h2>Inside the project</h2>{tags(p['stack'])}{external(p['repo'],'View on GitHub','button')}'''
    if p.get('demo'):
        content += external(p['demo'],'Open original demo','button button-quiet')
    content += f'''<a class="text-link" href="index.html#contact">Let's talk about it {ARROW}</a><p>{escape(p['note'])}</p></aside></div>
 <div class="related-project"><a href="project-{next_project['slug']}.html"><div><span class="overline">Next project</span><h2>{escape(next_project['title'])}</h2></div>{ARROW}</a></div>
</div></main>'''
    return content + footer()


def build():
    (ROOT/'index.html').write_text(home(),encoding='utf-8')
    (ROOT/'projects.html').write_text(projects_page(),encoding='utf-8')
    for i,p in enumerate(PROJECTS):
        (ROOT/f'project-{p["slug"]}.html').write_text(detail(p,PROJECTS[(i+1)%len(PROJECTS)]),encoding='utf-8')
    print(f'Generated homepage, project index, and {len(PROJECTS)} project pages.')


if __name__ == '__main__':
    build()
