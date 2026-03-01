"""Generate cv.xlsx from Jason Edward Lewis CV data."""
import openpyxl
from openpyxl import Workbook
from pathlib import Path

wb = Workbook()
ws = wb.active
ws.title = "CV"

headers = ["start date", "end date", "headline", "description", "project", "group", "org", "program"]
ws.append(headers)

PRESENT = "02/25/2026"

GRP_ORDER = [
    "Employment", "Honors", "Education", "Creative Works", "Books/Chapters",
    "Journal Articles", "Keynotes", "Solo Exhibitions",
    "Group Exhibitions", "Productions",
    "Funding (PI)", "Funding (Co-I)", "Funding (Internal)",
    "Courses Taught", "Supervision", "Service",
]

rows = [

    # ── EMPLOYMENT ─────────────────────────────────────────────────────────
    ("06/01/2019", PRESENT,
     "Special Advisor to the Provost, Indigenous Spaces and Donor Relations",
     "Concordia University, Montreal, QC",
     "Concordia", "Employment"),

    ("06/01/2014", PRESENT,
     "University Research Chair (Tier 1) in Computational Media and the Indigenous Future Imaginary",
     "Concordia University, Montreal, QC",
     "Concordia", "Employment"),

    ("06/01/2014", PRESENT,
     "Professor of Computation Arts",
     "Dept. of Design and Computation Arts, Faculty of Fine Arts, Concordia University",
     "Concordia", "Employment"),

    ("06/01/2008", "05/31/2014",
     "Associate Professor of Computation Arts",
     "Dept. of Design and Computation Arts, Faculty of Fine Arts, Concordia University",
     "Concordia", "Employment"),

    ("09/01/2008", "12/31/2013",
     "Director, Computation Arts Program",
     "Dept. of Design and Computation Arts, Faculty of Fine Arts, Concordia University",
     "Concordia", "Employment"),

    ("09/01/2002", "05/31/2007",
     "Assistant Professor of Computation Arts",
     "Dept. of Design and Computation Arts, Faculty of Fine Arts, Concordia University",
     "Concordia", "Employment"),

    ("09/01/1999", "08/31/2001",
     "Founder and Director of Research, Arts Alliance Laboratory",
     "San Francisco, CA",
     "Early Career", "Employment"),

    ("05/01/1997", "08/31/2003",
     "Advisor, Arts Alliance Ventures",
     "London, England",
     "Early Career", "Employment"),

    ("09/01/1996", "08/31/1999",
     "Member of Research Staff, Interval Research Corporation",
     "Palo Alto, CA",
     "Early Career", "Employment"),

    ("06/01/1995", "09/30/1995",
     "Interaction Designer, Fitch, Inc.",
     "San Francisco, CA",
     "Early Career", "Employment"),

    ("05/01/1994", "09/30/1994",
     "Conceptualizer, Associate Producer & Research Coordinator — Electric Carnival, Lollapalooza '94",
     "North American Tour",
     "Early Career", "Employment"),

    ("10/01/1993", "09/30/1994",
     "Interaction Designer, Interval Research Corporation",
     "Palo Alto, CA",
     "Early Career", "Employment"),

    ("09/01/1992", "09/30/1993",
     "Carnegie Research Fellow, Institute for Research on Learning",
     "Palo Alto, CA",
     "Early Career", "Employment"),

    ("04/01/1992", "06/30/1992",
     "Instructor, Stanford University — 'Critical Theories for an Electric Society'",
     "Undergraduate Special Course, Stanford, CA",
     "Early Career", "Employment"),

    # ── EDUCATION ──────────────────────────────────────────────────────────
    ("09/01/1994", "06/30/1997",
     "M.Phil. Design, Royal College of Art",
     "London, England",
     "Early Career", "Education"),

    ("09/01/1987", "06/30/1988",
     "Philosophy & Critical Theory, Freie Universität Berlin",
     "West Germany — DAAD Fellowship",
     "Early Career", "Education"),

    ("09/01/1985", "06/30/1991",
     "B.S. Symbolic Systems (Cognitive Science) + B.A. German Studies, Stanford University",
     "Palo Alto, CA",
     "Early Career", "Education"),

    # ── HONORS & AWARDS ────────────────────────────────────────────────────
    ("01/01/2025", "01/01/2025",
     "Jane Lombard Fellowship",
     "", "Recognition", "Honors"),

    ("01/01/2025", "01/01/2025",
     "SSHRC Impact Partnership Award",
     "Social Sciences and Humanities Research Council",
     "Recognition", "Honors"),

    ("01/01/2024", "01/01/2024",
     "SSHRC Impact Partnership Award Finalist",
     "", "Recognition", "Honors"),

    ("01/01/2023", "01/01/2023",
     "Outstanding Staff and Faculty Award, Concordia Alumni Association",
     "", "Recognition", "Honors"),

    ("01/01/2023", "01/01/2023",
     "American Indian Film Festival — Nominee, Best Animated Short (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2022", "01/01/2022",
     "Provost Circle of Distinction, Concordia University",
     "", "Recognition", "Honors"),

    ("01/01/2021", "01/01/2021",
     "Fellow of the Royal Society of Canada",
     "", "Recognition", "Honors"),

    ("01/01/2021", "01/01/2021",
     "SAIO 50 for 50, Stanford American Indian Organization",
     "", "Recognition", "Honors"),

    ("01/01/2020", "01/01/2020",
     "Concordia University Research Chair Tier 1 (renewed)",
     "", "Recognition", "Honors"),

    ("01/01/2019", "01/01/2019",
     "IndieCade Festival — Nominee, Best Performance (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2018", "01/01/2018",
     "MIT Press Resisting Reduction Essay Competition — Winner",
     "", "Recognition", "Honors"),

    ("01/01/2018", "01/01/2018",
     "Prix Ars Electronica — Honorary Mention",
     "", "Recognition", "Honors"),

    ("01/01/2015", "01/01/2015",
     "ELO Collection vol. 3 — Selection",
     "Electronic Literature Organization", "Recognition", "Honors"),

    ("01/01/2014", "01/01/2014",
     "Trudeau Foundation Fellowship",
     "", "Recognition", "Honors"),

    ("01/01/2014", "01/01/2014",
     "Concordia University Research Chair Tier 1",
     "", "Recognition", "Honors"),

    ("01/01/2014", "01/01/2014",
     "Great Concordians",
     "Concordia University", "Recognition", "Honors"),

    ("01/01/2014", "01/01/2014",
     "Inaugural Robert Coover Award — Best Work of Electronic Literature",
     "Electronic Literature Organization", "Recognition", "Honors"),

    ("01/01/2013", "01/01/2013",
     "imagineNATIVE Festival — Best New Media (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2012", "01/01/2012",
     "Ashoka Changemakers Award, J.W. McConnell Family Foundation",
     "", "Recognition", "Honors"),

    ("01/01/2012", "01/01/2012",
     "Electronic Literature Organization — Jury Award",
     "", "Recognition", "Honors"),

    ("01/01/2011", "01/01/2011",
     "ELO Collection vol. 2 — Selection",
     "", "Recognition", "Honors"),

    ("01/01/2010", "01/01/2010",
     "imagineNATIVE Festival — Best New Media (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2009", "01/01/2009",
     "imagineNATIVE Festival — Best New Media (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2000", "01/01/2000",
     "Prix Ars Electronica — Honorary Mention",
     "Digital Language, FILE Festival", "Recognition", "Honors"),

    ("01/01/1994", "01/01/1994",
     "Royal College of Art Scholarship",
     "", "Recognition", "Honors"),

    ("01/01/1986", "01/01/1986",
     "Freie Universität – Stanford University DAAD Fellowship",
     "", "Recognition", "Honors"),

    # ── CREATIVE WORKS (P.o.E.M.M. + major installations) ─────────────────
    ("01/01/1995", "12/31/1995",
     "Aura",
     "Interactive installation. With E. Brechin and R. Strein. Mac OS, custom electronics, metal plinth, video projector, vellum.",
     "Creative", "Creative Works"),

    ("01/01/1996", "12/31/1996",
     "WordNozzle: Firehose",
     "Interactive installation. Mac OS, custom Lingo, firehose, nozzle, projection, custom electronics.",
     "Creative", "Creative Works"),

    ("01/01/1999", "12/31/1999",
     "I Know What You're Thinking",
     "Screen interactive. Mac OS, custom Lingo.",
     "Creative", "Creative Works"),

    ("01/01/2000", "12/31/2000",
     "ActiveText: The Installation",
     "With A. Weyers. Interactive installation. Windows OS, custom C++.",
     "Creative", "Creative Works"),

    ("01/01/2002", "12/31/2002",
     "Thanksgiving Address: Greetings to the Technological World",
     "Screen interactive. Flash, custom Actionscript. Co-created with S. T. Fragnito.",
     "AbTeC", "Creative Works"),

    ("01/01/2005", "12/31/2005",
     "Cityspeak",
     "Massively multi-user public space chat system. With B. Nadeau, M. Lévesque, E. Zananiri and L. Bellemare.",
     "Creative", "Creative Works"),

    ("01/01/2007", "12/31/2007",
     "What They Speak When They Speak To Me",
     "With B. Nadeau & E. Zananiri. Interactive touchwork. Windows OS, custom Java.",
     "Creative", "Creative Works"),

    ("01/01/2007", "12/31/2007",
     "Intralocutor",
     "With Y. Assogba, D. Bouchard, and B. Nadeau. Interactive installation. Windows OS, custom Java, projection.",
     "Creative", "Creative Works"),

    ("01/01/2010", "12/31/2010",
     "The Great Migration",
     "With B. Nadeau and C. Dupont. Interactive touchwork with large-scale print. Mac OS, custom Java.",
     "Creative", "Creative Works"),

    ("01/01/2010", "12/31/2010",
     "Migration (P.o.E.M.M.)",
     "With C. Dupont and B. Nadeau. Interactive touchwork poem for iPad/iPhone. iOS.",
     "Creative", "Creative Works"),

    ("01/01/2011", "12/31/2011",
     "White / Choice / Bastard (P.o.E.M.M.)",
     "Interactive touchwork poems. With C. Gratton, S. Maheu and B. Nadeau. iOS, Objective-C.",
     "Creative", "Creative Works"),

    ("01/01/2011", "12/31/2011",
     "No Choice About the Terminology",
     "With E. Zananiri and B. Nadeau. Interactive touchwork with large-scale print. Commissioned by imagineNATIVE.",
     "Creative", "Creative Works"),

    ("01/01/2012", "12/31/2012",
     "Rattlesnakes (P.o.E.M.M.)",
     "With S. Maheu and B. Nadeau. Interactive touchwork poem for iPad/iPhone. iOS, Objective-C.",
     "Creative", "Creative Works"),

    ("01/01/2012", "12/31/2012",
     "The Summer the Rattlesnakes Came",
     "With B. Nadeau. Interactive touchwork with large-scale print. Mac OS, custom Java.",
     "Creative", "Creative Works"),

    ("01/01/2013", "12/31/2013",
     "Death (P.o.E.M.M.)",
     "With S. Maheu and B. Nadeau. Interactive touchwork poem for iPad/iPhone. iOS, Objective-C.",
     "Creative", "Creative Works"),

    ("01/01/2013", "12/31/2013",
     "The World That Surrounds You Wants Your Death",
     "With B. Nadeau. Interactive touchwork with large-scale print. Mac OS, custom Java.",
     "Creative", "Creative Works"),

    # ── BOOKS/CHAPTERS ─────────────────────────────────────────────────────
    ("01/01/2021", "01/01/2021",
     "Against Reduction: Designing a Human Future with Machines",
     "Co-edited with Noelani Arista, Sasha Costanza-Chock, Suzanne Kite et al. Cambridge, MA: The MIT Press.",
     "Research", "Books/Chapters"),

    ("01/01/2014", "01/01/2014",
     "Educational, Psychological, and Behavioral Considerations in Niche Online Communities",
     "Co-edited with Vivek Venkatesh, Jason Wallin, Juan Carlos Castro. Hershey: IGI Global Press.",
     "Research", "Books/Chapters"),

    # ── JOURNAL ARTICLES & PROCEEDINGS ────────────────────────────────────
    ("01/01/2024", "01/01/2024",
     "Abundant Intelligences: Placing AI Within Indigenous Knowledge Frameworks",
     "With Hēmi Whaanga and Ceyda Yolgörmez. AI & Society. doi.org/10.1007/s00146-024-02099-4",
     "Research", "Journal Articles"),

    ("01/01/2018", "01/01/2018",
     "Making Kin with the Machines",
     "With Noelani Arista, Archer Pechawis and Suzanne Kite. Journal of Design and Science, Issue 3.5. doi.org/10.21428/bfafd97b",
     "Research", "Journal Articles"),

    ("01/01/2018", "01/01/2018",
     "The Future is Indigenous",
     "With Skawennati. Leonardo 51, No. 4 (pp. 422–423).",
     "Research", "Journal Articles"),

    ("01/01/2012", "01/01/2012",
     "Art Work as Argument",
     "With Skawennati. Canadian Journal of Communications, Vol. 37 No. 1.",
     "Research", "Journal Articles"),

    ("01/01/2011", "01/01/2011",
     "Skins: Designing Games with First Nations Youth",
     "With Beth Aileen Lameman. Journal of Game Design and Development Education, Vol. 1 No. 1.",
     "AbTeC", "Journal Articles"),

    ("01/01/2010", "01/01/2010",
     "Post PostScript Please",
     "With Bruno Nadeau. Digital Creativity vol. 21, no. 1 (pp. 18–29).",
     "Creative", "Journal Articles"),

    ("01/01/2008", "01/01/2008",
     "Writing-Designing-Programming",
     "Media-Space Journal: Special Issue on Futures of New Media Art, Vol 1 no. 1.",
     "Research", "Journal Articles"),

    ("01/01/2006", "01/01/2006",
     "Taking Sides: Dynamic Text and Hip-Hop Performance",
     "With Yannick Assogba. Proceedings of the 14th ACM International Conference on Multimedia.",
     "Creative", "Journal Articles"),

    ("01/01/1999", "01/01/1999",
     "ActiveText: A Method for Creating Dynamic and Interactive Texts",
     "With Alex Weyers. Proceedings of UIST 1999.",
     "Creative", "Journal Articles"),

    # ── BOOK CHAPTERS ──────────────────────────────────────────────────────
    ("01/01/2026", "01/01/2026",
     "Before Intelligence",
     "With Suzanne Kite and Scott Benesiinaabandan. All Watched Over by Machines of Loving Grace catalog, PST ART: Art & Science Collide, REDCAT/CalArts, Los Angeles. In press.",
     "Research", "Books/Chapters"),

    ("01/01/2026", "01/01/2026",
     "Imagining Otherwise",
     "With Suzanne Kite and Scott Benesiinaabandan. In Syrus Marcus Ware et al. (Eds.), The Art History Book We Wish We Had: IBPOC artmaking in Northern Turtle Island. Revised and Submitted.",
     "Research", "Books/Chapters"),

    ("01/01/2025", "01/01/2025",
     "Reworlding AI Through Future Imaginaries",
     "With Ceyda Yolgörmez. In Philipp Hacker (Ed.), Oxford Intersections: AI in Society. Oxford: Oxford Academic. doi.org/10.1093/9780198945215.003.0166",
     "Research", "Books/Chapters"),

    ("01/01/2025", "01/01/2025",
     "The Indigenous Protocol and AI Workshops as Future Imaginary",
     "In Carolyn F. Strauss (Ed.), Slow Technology Reader. Amsterdam: Valiz.",
     "IIF", "Books/Chapters"),

    ("01/01/2025", "01/01/2025",
     "CyberPowWow and the First Wave of Indigenous Digital Media Arts",
     "With Mikhel Proulx. In Karmen Cray and Joanna Hearne (Eds.), By Their Work: Indigenous Women's Digital Media in North America. University of Minnesota Press.",
     "AbTeC", "Books/Chapters"),

    ("01/01/2024", "01/01/2024",
     "The Myths of My Descendents",
     "In Amy Scott (Ed.), Future Imaginaries: Indigenous Art, Fashion, and Technology catalog, PST ART, Autry Museum of the American West, Los Angeles.",
     "IIF", "Books/Chapters"),

    ("01/01/2024", "01/01/2024",
     "Building Aboriginal Territories in Cyberspace",
     "With Skawennati. In Monika Kin Gagnon and Brandon Webb (Eds.), Concordia University at 50: A Collective History. Montreal: Concordia University Press.",
     "AbTeC", "Books/Chapters"),

    ("01/01/2023", "01/01/2023",
     "Good Technology is Messy",
     "In Eleanor Drage and Kerry Mckereth (Eds.), The Good Robot: Why Technologies of the Future Need Feminism (pp. 21–27). London: Bloomsbury Press.",
     "Research", "Books/Chapters"),

    ("01/01/2023", "01/01/2023",
     "Making Kin with the Machines (Oxford reprint)",
     "With Noelani Arista, Archer Pechawis, and Suzanne Kite. In S. Cave, E. Drage and K. Mckereth (Eds.), Feminist AI. Oxford: Oxford University Press.",
     "Research", "Books/Chapters"),

    ("01/01/2023", "01/01/2023",
     "The Future Imaginary",
     "In Routledge Handbook of CoFuturisms (pp. 11–22). B. Chattopadhyay et al. (Eds.). New York: Routledge. doi.org/10.4324/9780429317828",
     "IIF", "Books/Chapters"),

    ("01/01/2023", "01/01/2023",
     "Imagining Indigenous AI",
     "In Stephen Cave and Kanta Dihal (Eds.), Imagining AI: How the World Sees Intelligent Machines (pp. 210–217). Oxford: Oxford University Press.",
     "IIF", "Books/Chapters"),

    ("01/01/2023", "01/01/2023",
     "Relation-Oriented AI: Why Indigenous Protocols Matter for the Digital Humanities",
     "With Michelle Lee Smith and Hémi Whaanga. In Debates in Digital Humanities 2023 (pp. 74–83). University of Minnesota Press.",
     "Research", "Books/Chapters"),

    ("01/01/2022", "01/01/2022",
     "Overclock Our Imagination! Mapping the Indigenous Future Imaginary",
     "In Igloliorte and Taunton (Eds.), The Routledge Companion to Indigenous Art Histories in the United States and Canada (pp. 64–75).",
     "IIF", "Books/Chapters"),

    ("01/01/2021", "01/01/2021",
     "Making Kin with the Machines (Atlas of Anomalous AI reprint)",
     "With Noelani Arista, Archer Pechawis, and Suzanne Kite. In Ben Vickers and K Allado-McDowell (Eds.), Atlas of Anomalous AI (pp. 40–51). London: Ignota Press.",
     "Research", "Books/Chapters"),

    ("01/01/2020", "01/01/2020",
     "22nd-Century Proto:typing",
     "In Dickenson, Hill and Lalonde (Eds.), Àbadakone/Continuous Fire/Feu Continuel Exhibition Catalog (pp. 125–132). Ottawa: National Gallery of Canada.",
     "IIF", "Books/Chapters"),

    ("01/01/2019", "01/01/2019",
     "Future Imaginary Dialogue with Dr. Kim TallBear",
     "In Deanna Brown (Ed.), Other Places: Writings on Media Arts Practices in Canada (pp. 10–27). Toronto: Media Arts Network of Ontario.",
     "IIF", "Books/Chapters"),

    ("01/01/2019", "01/01/2019",
     "An Orderly Assemblage of Biases: Troubling the Monocultural Stack",
     "In Schweitzer and Henry (Eds.), Afterlives of Indigenous Archives (pp. 219–231). Lebanon: University Press of New England.",
     "Research", "Books/Chapters"),

    ("01/01/2016", "01/01/2016",
     "Preparations for a Haunting: Notes Towards an Indigenous Future Imaginary",
     "In Barney et al. (Eds.), The Participatory Condition in the Digital Age (pp. 229–249). Minneapolis: University of Minnesota Press.",
     "IIF", "Books/Chapters"),

    ("01/01/2014", "01/01/2014",
     "A Better Dance and Better Prayers: Systems, Structures, and the Future Imaginary in Aboriginal New Media",
     "In Steve Loft and Kerry Swanson (Eds.), Coded Territories: Tracing Indigenous Pathways in New Media (pp. 48–77). Calgary: University of Alberta Press.",
     "AbTeC", "Books/Chapters"),

    ("01/01/2014", "01/01/2014",
     "Grand Theft Rez: Building and Maintaining a Community for the Skins Workshops",
     "With Skawennati. In Pleasants and Salter (Eds.), Community-Based Multiliteracies and Digital Media Projects (pp. 111–136). New York: Peter Lang Publishing.",
     "AbTeC", "Books/Chapters"),

    ("01/01/2013", "01/01/2013",
     "TimeTraveller™: First Nations Nonverbal Communication in Second Life",
     "With Elizabeth Aileen LaPensée. In Tanenbaum et al. (Eds.), Nonverbal Communications in Virtual Worlds (pp. 94–107). Pittsburgh: ETC Press.",
     "AbTeC", "Books/Chapters"),

    ("01/01/2013", "01/01/2013",
     "Call it a Vision Quest: Machinima in a First Nations Context",
     "With Elizabeth Aileen LaPensée. In Jenna Ng (Ed.), Understanding Machinima (pp. 187–206). New York: Continuum Press.",
     "AbTeC", "Books/Chapters"),

    ("01/01/2008", "01/01/2008",
     "(Im)mobile Nation",
     "With Maroussia Lévesque. In Ladly and Beesley (Eds.), Mobile Nation: Creating Methodologies for Mobile Platforms (pp. 141–147). Toronto: Riverside Architectural Press.",
     "Creative", "Books/Chapters"),

    # ── KEYNOTES ───────────────────────────────────────────────────────────
    ("03/02/2023", "03/02/2023",
     "Keynote: Future Imaginaries of Abundant Intelligences",
     "Interaction 23, Zürich, Switzerland.",
     "IIF", "Keynotes"),

    ("10/22/2021", "10/22/2021",
     "Keynote: Creating Future Imaginaries through Indigenous AI",
     "EPIC Conference 2021. Ethnopraxis in Industry.",
     "IIF", "Keynotes"),

    ("09/24/2021", "09/24/2021",
     "Keynote: 22nd-Century Proto-typing",
     "PIVOT 2021, Pluriversal Design SIG / OCAD University, Toronto, ON.",
     "IIF", "Keynotes"),

    ("01/23/2021", "01/23/2021",
     "Marshall McLuhan Lecture: Expansive, Embracing, Evolving — Beyond Impoverished Intelligences",
     "Transmediale Festival, Berlin, Germany.",
     "IIF", "Keynotes"),

    ("08/21/2019", "08/21/2019",
     "Keynote: Making Kin with the Machines",
     "With Suzanne Kite. MUTEK Festival, Montreal, QC.",
     "IIF", "Keynotes"),

    ("10/10/2018", "10/10/2018",
     "Keynote: White Supremacy — It's Not Just for People Anymore!",
     "Association of Internet Researchers (AoIR), UQAM, Montreal, QC.",
     "Research", "Keynotes"),

    ("08/13/2018", "08/18/2018",
     "Keynote: Mod Cyberspace, Mod the World!",
     "With Skawennati. Electronic Literature Organization Annual Conference, UQAM, Montreal, QC.",
     "Creative", "Keynotes"),

    ("10/31/2017", "10/31/2017",
     "Opening Keynote: Decolonizing Immersive Media",
     "Enterprising Culture Conference, CFC Media Lab, Corus Quay, Toronto, ON.",
     "IIF", "Keynotes"),

    ("10/28/2016", "10/28/2016",
     "Keynote: An Orderly Assemblage of Biases — Computation as Cultural Material",
     "Crossing Boundaries, University of Lethbridge, AB.",
     "Research", "Keynotes"),

    ("10/06/2016", "10/06/2016",
     "Keynote: Populating the Future Imaginary — Visualizing Indigenous Futures",
     "International Visual Literacy Association Annual Conference, Concordia University, Montreal, QC.",
     "IIF", "Keynotes"),

    ("02/01/2014", "02/28/2014",
     "Keynote: The P.o.E.M.M. Cycle — First Reflections",
     "New Oceania Literary Series, University of Hawai'i at Mānoa, Honolulu, HI.",
     "Creative", "Keynotes"),

    ("09/14/2013", "09/14/2013",
     "Talk: The Future Imaginary",
     "TEDxMontreal 2013, Société des Arts Technologiques, Montréal, QC.",
     "IIF", "Keynotes"),

    # ── SOLO EXHIBITIONS ───────────────────────────────────────────────────
    ("11/04/2017", "12/02/2017",
     "Owerà:ke Non Aié:nahne / Filling in the Blank Spaces / Combler les espaces vides: An AbTeC Retrospective",
     "Leonard & Bina Ellen Gallery, Montreal, QC.",
     "AbTeC", "Solo Exhibitions"),

    ("05/01/2015", "06/30/2015",
     "His Blood, In Search of a Face (The P.o.E.M.M. Cycle)",
     "DHC/Art & the PHI Centre, Montreal, QC.",
     "Creative", "Solo Exhibitions"),

    ("09/01/2012", "09/30/2012",
     "Touch: The Art of the Mobile App",
     "Nouspace Gallery & Media Lounge, Vancouver, WA.",
     "Creative", "Solo Exhibitions"),

    ("10/01/2011", "10/31/2011",
     "Vital to the General Public Welfare",
     "Edward Day Gallery & imagineNATIVE Festival, Toronto, ON.",
     "Creative", "Solo Exhibitions"),

    ("03/01/2011", "04/30/2011",
     "Words Found on an Empty Beach",
     "ArtEngine, Ottawa, ON.",
     "Creative", "Solo Exhibitions"),

    ("06/01/2010", "06/30/2010",
     "Things You've Said Before But We Never Heard",
     "FOFA Gallery, Montreal, QC.",
     "Creative", "Solo Exhibitions"),

    ("02/01/2007", "03/31/2007",
     "Everything You'd Thought We'd Forgotten",
     "OBORO, Montreal, QC.",
     "Creative", "Solo Exhibitions"),

    # ── GROUP EXHIBITIONS (selected) ───────────────────────────────────────
    ("09/17/2022", "12/11/2022",
     "Poets with a Video Camera: Videopoetry 1980–2020",
     "Surrey Art Gallery, Surrey, B.C. Curator: Tom Konyves.",
     "Creative", "Group Exhibitions"),

    ("04/23/2020", "06/21/2020",
     "Kahwatsiretátie: Teionkwariwaienna Tekariwaiennawahkòntie",
     "Biennale d'art contemporain autochtone, Montreal.",
     "AbTeC", "Group Exhibitions"),

    ("01/01/2016", "04/30/2016",
     "Electronic Literature: A Matter of Bits",
     "Stedman Gallery, Rutgers-Camden Center for the Arts, Camden NJ. Curator: Jim Brown.",
     "Creative", "Group Exhibitions"),

    ("06/01/2014", "09/30/2014",
     "Poetic Codings (San Jose ICA)",
     "San Jose Institute of Contemporary Art, San Jose, CA. Curator: Jody Zellen.",
     "Creative", "Group Exhibitions"),

    ("09/01/2013", "09/30/2013",
     "Les littératures numériques d'hier à demain",
     "Bibliothèque Nationale Française, Paris, France.",
     "Creative", "Group Exhibitions"),

    ("07/01/2013", "09/30/2013",
     "Signs for Sounds (Sunderland)",
     "Sunderland Museum and Art Gallery, Sunderland, U.K. Curator: Jeremy Theophilus.",
     "Creative", "Group Exhibitions"),

    ("06/01/2008", "08/31/2008",
     "SEND: Conversations in Evolving Media",
     "Institute for Contemporary Art, Portland, ME. Curator: Linda L. Lambertson.",
     "Creative", "Group Exhibitions"),

    ("07/01/2007", "08/31/2008",
     "Terminal Zero One",
     "International Terminal, Pearson International Airport, Toronto, ON. Year Zero One Collective.",
     "Creative", "Group Exhibitions"),

    ("09/01/2000", "08/31/2002",
     "Print on Screen",
     "Ars Electronica Center, Linz, Austria.",
     "Creative", "Group Exhibitions"),

    ("03/01/1995", "03/31/1995",
     "SelfStorage",
     "Curators: Laurie Anderson and Brian Eno. Art Angel, Wimberley, London, England.",
     "Creative", "Group Exhibitions"),

    # ── PRODUCTIONS (AbTeC / Skins) ────────────────────────────────────────
    ("09/01/2008", "06/30/2009",
     "Skins 1.0: Workshop on Aboriginal Storytelling and Video Game Design",
     "With Skawennati. Kahnawake Survival School, Kahnawake First Nation, QC.",
     "AbTeC", "Productions"),

    ("08/01/2011", "08/31/2011",
     "Skins 2.0: Summer Institute on Aboriginal Storytelling and Video Game Design",
     "With Skawennati. Concordia University, Montreal, QC.",
     "AbTeC", "Productions"),

    ("03/01/2012", "08/31/2012",
     "Skins 3.0: Extended Play",
     "With Skawennati. Concordia University & Kahnawake Education Centre.",
     "AbTeC", "Productions"),

    ("05/01/2013", "06/30/2013",
     "Skins 4.0: World Domination",
     "With Skawennati. Concordia University & Kahnawake Education Centre.",
     "AbTeC", "Productions"),

    ("07/01/2017", "08/31/2017",
     "Skins 5.0: Kanaeokana/He Au Hou — Making Mo'olelo Through Video Games",
     "With Skawennati. Hālau 'Īnana, Kamehameha Schools, Honolulu, HI.",
     "AbTeC", "Productions"),

    ("07/01/2017", "08/31/2017",
     "Skins 6.0: Making Mo'olelo Through Video Games 2",
     "With Skawennati. Hālau 'Īnana, Kamehameha Schools, Honolulu, HI.",
     "AbTeC", "Productions"),

    ("01/01/2009", PRESENT,
     "AbTeC Island",
     "Second Life island and exhibition venue. Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2009", "12/31/2009",
     "Otsi:! Rise of the Kanien'keha:ka Legends",
     "Video game. Unreal Engine. Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2011", "12/31/2011",
     "The Adventure of Skahion:ati: Legend of the Stone Giants",
     "Video game. Unity 3D. Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2012", "12/31/2012",
     "Skahion:ati: Rise of the Kanien'keha:ka Legends",
     "Video game. Unity. Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2011", "12/31/2013",
     "TimeTraveller™ (Episodes I–IX)",
     "Machinima series with Skawennati. Second Life. Montreal: Aboriginal Territories in Cyberspace. Executive Producer.",
     "AbTeC", "Productions"),

    ("01/01/2013", "12/31/2013",
     "Ienién:te and the Peacemaker's Wampum",
     "Video game. Construct 2. Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2017", "12/31/2017",
     "He Ao Hou: A New World",
     "Video game. Unity. Honolulu and Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2017", "12/31/2017",
     "Wao Kanaka: In the Realm of the Humans",
     "Video game. Unity. Honolulu and Montreal: Aboriginal Territories in Cyberspace.",
     "AbTeC", "Productions"),

    ("01/01/2017", "12/31/2017",
     "The Peacemaker Returns / She Falls for Ages",
     "Machinima by Skawennati. Second Life. Montreal: Aboriginal Territories in Cyberspace. Executive Producer.",
     "AbTeC", "Productions"),

    ("01/01/2022", "12/31/2022",
     "When the Earth Began: The Way of the Skydwellers",
     "Film. Kanien'kehá:ka Onkwawén:na Raotitióhkwa Language and Cultural Center & AbTeC. Executive Producer.",
     "AbTeC", "Productions"),

    ("01/01/2022", "12/31/2022",
     "Past Future Forward: The Making of a Hawaiian Video Game",
     "Film. Director & Producer. Hawaiian International Film Festival (HIFF), Nov. 2022.",
     "AbTeC", "Productions"),

    # ── FUNDING (PI) — EXTERNAL ────────────────────────────────────────────
    ("11/24/2025", "11/24/2025",
     "Impact Partnership Award",
     "$50,000. Social Sciences and Humanities Research Council.",
     "Recognition", "Funding (PI)"),

    ("04/01/2025", "03/31/2029",
     "Transmediating Indigenous Art",
     "$378,974. Social Sciences and Humanities Research Council.",
     "Research", "Funding (PI)"),

    ("08/15/2024", "08/14/2026",
     "An Abundant Data Trust",
     "$284,000. The Schmidt Family Foundation — 11th Hour Project.",
     "AI", "Funding (PI)"),

    ("03/01/2023", "02/28/2029",
     "Abundant Intelligences: Expanding AI through Indigenous Knowledge Systems",
     "$22,830,281. New Frontiers in Research Fund.",
     "AI", "Funding (PI)"),

    ("06/01/2023", "05/30/2025",
     "Foundations of Abundant Intelligences",
     "$675,000. The MacArthur Foundation.",
     "AI", "Funding (PI)"),

    ("04/01/2023", "03/31/2029",
     "Partnership for Abundant Intelligences",
     "$2,499,875. Social Sciences and Humanities Research Council.",
     "AI", "Funding (PI)"),

    ("04/01/2023", "03/31/2029",
     "Indigenous Futures Research Centre",
     "$450,609. Canada Foundation for Innovation.",
     "IIF", "Funding (PI)"),

    ("01/01/2023", "07/01/2023",
     "Abundant Intelligences Residency 1",
     "$26,000. Montalvo Arts Center.",
     "AI", "Funding (PI)"),

    ("08/15/2022", "08/14/2023",
     "Abundant Intelligences: Year 01",
     "$98,000. The Schmidt Family Foundation — 11th Hour Project.",
     "AI", "Funding (PI)"),

    ("03/15/2022", "10/30/2022",
     "Abundant Intelligences",
     "$20,000. Social Sciences and Humanities Research Council.",
     "AI", "Funding (PI)"),

    ("04/01/2022", "03/03/2024",
     "L'art autochtone dans les environnements virtuels",
     "$221,905. Fonds de recherche Société et culture Québec.",
     "AbTeC", "Funding (PI)"),

    ("01/15/2022", "01/15/2025",
     "Expanding Skins Workshops on Aboriginal Storytelling in Digital Media",
     "$498,000. Hewitt Foundation.",
     "AbTeC", "Funding (PI)"),

    ("01/25/2021", "03/30/2022",
     "Building Capacity with the Skins Workshops",
     "$30,000. Indigenous Screen Office.",
     "AbTeC", "Funding (PI)"),

    ("03/01/2019", "12/31/2019",
     "Building Indigenous Capacity & Community in Digital Media Sectors",
     "$250,000. Canada Council for the Arts. Co-lead.",
     "AbTeC", "Funding (PI)"),

    ("01/15/2019", "06/01/2019",
     "Indigenous Protocol and Artificial Intelligence Workshops",
     "$49,026. Social Sciences and Humanities Research Council.",
     "AI", "Funding (PI)"),

    ("09/01/2018", "06/01/2019",
     "Indigenous Protocol and Artificial Intelligence Workshops",
     "$80,000. Canadian Institute for Advanced Research.",
     "AI", "Funding (PI)"),

    ("04/01/2018", "12/31/2018",
     "Skins 6.0: Kanaeokana — Workshop on Aboriginal Storytelling and Video Game Design",
     "$389,000. Kanaeokana Network (Hawaii).",
     "AbTeC", "Funding (PI)"),

    ("04/01/2017", "12/31/2017",
     "Skins 5.0: Kanaeokana — Workshop on Aboriginal Storytelling and Video Game Design",
     "$187,000. Kanaeokana Network (Hawaii).",
     "AbTeC", "Funding (PI)"),

    ("07/01/2016", "07/01/2017",
     "Blueberry Pie in the Martian Sky",
     "$60,000. Canada Council for the Arts. Research Director / Executive Producer. Artist: Scott Benesiinaabandan.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2015", "03/31/2022",
     "Initiative for Indigenous Futures Partnership",
     "$2,491,613. Social Sciences and Humanities Research Council.",
     "IIF", "Funding (PI)"),

    ("06/01/2014", "05/31/2017",
     "Trudeau Fellowship",
     "$225,000. Pierre Elliott Trudeau Foundation.",
     "Recognition", "Funding (PI)"),

    ("06/01/2014", "11/03/2014",
     "Initiative for Indigenous Futures — Letter of Intent",
     "$20,000. Social Sciences and Humanities Research Council.",
     "IIF", "Funding (PI)"),

    ("07/01/2012", "09/30/2013",
     "The P.o.E.M.M. Cycle 6–10",
     "$58,000. Canada Council for the Arts. Artist.",
     "PoEMM", "Funding (PI)"),

    ("04/01/2012", "03/03/2015",
     "TyP3: Protocoles, Plateformes, et Publics pour textes digitaux",
     "$163,556. Fonds québécois de la recherche sur la société et la culture.",
     "Research", "Funding (PI)"),

    ("04/15/2012", "04/15/2013",
     "Skins Workshop",
     "$2,500. J. W. McConnell Family Foundation.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2012", "12/30/2013",
     "Abstracted Pow Wow",
     "$59,000. Canada Council for the Arts. Research Director / Executive Producer. Artist: Scott Benesiinaabandan.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2011", "03/30/2014",
     "Skins, Storytellers and Second Lives: A Partnership for Developing Aboriginal New Media",
     "$367,000. Social Sciences and Humanities Research Council.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2010", "06/30/2011",
     "Words Found on an Empty Beach",
     "$38,000. Canada Council for the Arts. Artist.",
     "Creative", "Funding (PI)"),

    ("07/01/2009", "06/30/2010",
     "TimeTraveller™",
     "$60,000. Canada Council for the Arts. Research Director / Executive Producer. Artist: Skawennati Tricia Fragnito.",
     "AbTeC", "Funding (PI)"),

    ("07/01/2009", "06/30/2012",
     "Ecriture complex: nouveaux modèles pour la typographie informatique",
     "$95,000. Fonds québécois de la recherche sur la société et la culture.",
     "Research", "Funding (PI)"),

    ("04/01/2009", "03/31/2012",
     "Building Aboriginal Territories in Cyberspace",
     "$149,000. Fonds québécois de la recherche sur la société et la culture.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2007", "03/31/2010",
     "Between Reading and Looking: Writing-Designing-Programming with Computational Media",
     "$193,000. Social Sciences and Humanities Research Council.",
     "Research", "Funding (PI)"),

    ("04/01/2006", "03/30/2009",
     "Aboriginal Territories in Cyberspace",
     "$239,000. Social Sciences and Humanities Research Council.",
     "AbTeC", "Funding (PI)"),

    ("06/01/2005", "01/06/2007",
     "Software for Interactive, Variable and Performative Texts",
     "$62,000. Hexagram Institute for Research/Creation in Media Arts and Technologies.",
     "Research", "Funding (PI)"),

    ("05/01/2004", "04/30/2007",
     "The Next Text",
     "$39,000. Fonds québécois de la recherche sur la société et la culture.",
     "Research", "Funding (PI)"),

    ("06/01/2004", "01/05/2005",
     "Writing the Next Text",
     "$39,000. Hexagram Institute for Research/Creation in Media Arts and Technologies.",
     "Research", "Funding (PI)"),

    ("01/15/1995", "09/30/1995",
     "Life is Bait",
     "$11,000. Arts Council of England. Co-grant holder.",
     "Early Career", "Funding (PI)"),

    # ── FUNDING (Co-I) — EXTERNAL ──────────────────────────────────────────
    ("04/01/2022", "03/30/2029",
     "R3AI: Shifting Paradigms for a Robust, Reasoning, & Responsible AI",
     "$124,000,000. Canada First Research Excellence Fund. Core Applicant. PI: Luc Vinet.",
     "Research", "Funding (Co-I)"),

    ("04/01/2022", "03/30/2024",
     "Meeting 30×30 and the Paris Agreement: Leveraging Digital Solutions for Nature-Based Solutions",
     "$256,623. Natural Sciences and Engineering Research Council. PI: Eliane Ubalijoro.",
     "Research", "Funding (Co-I)"),

    ("03/31/2022", "03/30/2028",
     "Infrastructure Beyond Extractivism: Material Approaches to Restoring Indigenous Jurisdiction",
     "$2,296,866. Social Sciences and Humanities Research Council. PI: Dayna Scott.",
     "IIF", "Funding (Co-I)"),

    ("03/31/2021", "03/30/2023",
     "Jurisdiction Back: Infrastructure beyond Extractivism",
     "$246,725. New Frontiers in Research Fund. PI: Dayna Scott.",
     "IIF", "Funding (Co-I)"),

    ("04/01/2020", "03/31/2027",
     "Hexagram Strategic Cluster",
     "$1,827,000. Fonds de recherche du Québec Société et culture. PI: Jean Dubois.",
     "Research", "Funding (Co-I)"),

    ("04/01/2019", "03/31/2024",
     "The Land as our Teacher: Land-based Pedagogy for/by Indigenous Youth",
     "$333,000. Social Sciences and Humanities Research Council. PI: Elizabeth Fast.",
     "AbTeC", "Funding (Co-I)"),

    ("04/01/2018", "12/31/2025",
     "Inuit Futures in Arts Leadership: The Pilimmaksarniq/Pijariuqsarniq Project",
     "$2,499,774. Social Sciences and Humanities Research Council. PI: Heather Igliolorte.",
     "IIF", "Funding (Co-I)"),

    ("04/01/2017", "03/23/2024",
     "Six Seasons of the Asiniskow Ithiniwak: Reclamation, Regeneration, and Reconciliation",
     "$2,500,000. Social Sciences and Humanities Research Council. PI: Mavis Reimer.",
     "IIF", "Funding (Co-I)"),

    ("04/01/2016", "03/23/2019",
     "A First Peoples Storytelling Exchange: Intersection College and Community Circles",
     "$240,000. Social Sciences and Humanities Research Council. PI: Susan Briscoe.",
     "AbTeC", "Funding (Co-I)"),

    ("04/01/2014", "03/03/2019",
     "HexagramCIAM – Centre Interuniversitaire des Arts Médiatiques",
     "$1,048,500. Fonds québécois de la recherche sur la société et la culture. PI: Christopher Salter.",
     "Research", "Funding (Co-I)"),

    ("04/01/2013", "03/30/2014",
     "GRAND: Graphics, Animation & New Media — Collaborating Network Investigator Grant",
     "$18,000. Networks of Centres of Excellence of Canada. PI: Kellogg Booth.",
     "Research", "Funding (Co-I)"),

    ("04/01/2012", "03/30/2013",
     "GRAND: Graphics, Animation & New Media — Collaborating Network Investigator Grant",
     "$10,000. Networks of Centres of Excellence of Canada. PI: Kellogg Booth.",
     "Research", "Funding (Co-I)"),

    ("04/01/2011", "03/30/2014",
     "Hexagram CIAM",
     "$367,000. Fonds Québécois de la Recherche sur la société et la culture. PIs: Nicolas Reeves, Giséle Trudel.",
     "Research", "Funding (Co-I)"),

    ("04/01/2011", "03/30/2012",
     "GRAND: Graphics, Animation & New Media — Collaborating Network Investigator Grant",
     "$6,000. Networks of Centres of Excellence of Canada. PI: Kellogg Booth.",
     "Research", "Funding (Co-I)"),

    ("04/01/2008", "03/31/2011",
     "Migration, Memory, Media: Emergent Technologies for Interactive Narrative Storytelling",
     "$119,000. Fonds québécois de la recherche sur la société et la culture. PI: Matt Soar.",
     "Research", "Funding (Co-I)"),

    ("04/01/2006", "03/30/2007",
     "Mobile Digital Commons Network Phase II",
     "$1,152,000. Heritage Canada. PIs: Michael Longford, Sara Diamond.",
     "Research", "Funding (Co-I)"),

    ("05/01/2004", "04/30/2007",
     "Expanding the Interface",
     "$135,000. Fonds québécois de la recherche sur la société et la culture. PI: Michael Longford.",
     "Research", "Funding (Co-I)"),

    ("08/01/2004", "03/31/2005",
     "Mobile Digital Commons Network",
     "$422,000. Heritage Canada. PIs: Michael Longford, Sara Diamond.",
     "Research", "Funding (Co-I)"),

    # ── FUNDING (INTERNAL) ─────────────────────────────────────────────────
    ("06/01/2019", "05/31/2025",
     "Concordia University Research Chair (Tier 1)",
     "$275,000. Concordia University.",
     "Concordia", "Funding (Internal)"),

    ("02/13/2019", "10/02/2019",
     "Archiving Indigenous Digital Arts Conference",
     "$1,800. Centre for Interdisciplinary Studies in Culture and Society, Concordia University.",
     "Concordia", "Funding (Internal)"),

    ("10/01/2019", "10/01/2019",
     "Archiving Indigenous Digital Arts Conference",
     "$5,965. Gail and Stephen A. Jarislowsky Institute for Studies in Canadian Art.",
     "Concordia", "Funding (Internal)"),

    ("10/31/2017", "08/01/2018",
     "Future Imaginary Lecture Series",
     "$5,000. Concordia University.",
     "IIF", "Funding (Internal)"),

    ("11/01/2016", "10/31/2017",
     "Aid to Research Related Events — Future Imaginary Lecture Series",
     "$5,000. Concordia University.",
     "IIF", "Funding (Internal)"),

    ("06/01/2014", "05/31/2019",
     "Concordia University Research Chair (Tier 1)",
     "$275,000. Concordia University.",
     "Concordia", "Funding (Internal)"),

    ("10/01/2012", "09/30/2014",
     "Game Designer-in-Residency Program",
     "$100,000. Office of Research, Research Development Fund.",
     "Concordia", "Funding (Internal)"),

    ("01/10/2012", "09/30/2014",
     "Strategy to Frame and Strengthen Production Based Game Research",
     "$50,000. Concordia University.",
     "Concordia", "Funding (Internal)"),

    ("01/11/2011", "10/31/2012",
     "Vital to the General Public Welfare: An Exhibition of Research/Creation Outcomes",
     "$5,000. Concordia University.",
     "Creative", "Funding (Internal)"),

    ("10/01/2010", "09/30/2011",
     "Aboriginal Territories in Cyberspace: First Contact",
     "$5,000. Office of Research ARRE.",
     "AbTeC", "Funding (Internal)"),

    ("03/18/2010", "03/30/2010",
     "Skins Summer Institute",
     "$100,000. Office of Research, Research Development Fund. Co-investigator: Skawennati Tricia Fragnito.",
     "AbTeC", "Funding (Internal)"),

    ("01/01/2004", "12/31/2011",
     "SSHRC Travel Grants",
     "$10,000. Fine Arts Faculty. Six separate grants.",
     "Research", "Funding (Internal)"),

    ("04/01/2004", "03/30/2005",
     "Participatory Tangible Board",
     "$50,000. Fine Arts-Engineering Seed Grants.",
     "Research", "Funding (Internal)"),

    ("04/01/2004", "03/30/2005",
     "Saying Red: Integrating Video Objects and Dynamic Typography",
     "$50,000. Fine Arts-Engineering Seed Grants.",
     "Creative", "Funding (Internal)"),

    ("01/01/2004", "12/31/2008",
     "Hexagram Travel Grants",
     "$8,000. Fine Arts Faculty. Four separate grants.",
     "Research", "Funding (Internal)"),

    # ── COURSES TAUGHT ─────────────────────────────────────────────────────
    ("01/01/2024", "04/30/2024",
     "DART634 Indigenous Futurisms",
     "Graduate seminar. Concordia University, Winter 2024.",
     "Concordia", "Courses Taught"),

    ("01/01/2023", "04/30/2023",
     "DART634 Indigenous Futurisms",
     "Graduate seminar. Concordia University, Winter 2023.",
     "Concordia", "Courses Taught"),

    ("01/01/2023", "04/30/2023",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2023.",
     "Concordia", "Courses Taught"),

    ("01/01/2022", "04/30/2022",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2022.",
     "Concordia", "Courses Taught"),

    ("01/01/2021", "04/30/2021",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2021.",
     "Concordia", "Courses Taught"),

    ("01/01/2019", "04/30/2019",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2019.",
     "Concordia", "Courses Taught"),

    ("09/01/2018", "12/31/2018",
     "CART 345 Computational Texts and Typography I",
     "Undergraduate course. Concordia University, Fall 2018.",
     "Concordia", "Courses Taught"),

    ("01/01/2018", "04/30/2018",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2018.",
     "Concordia", "Courses Taught"),

    ("09/01/2017", "12/31/2017",
     "CART 345 Computational Texts and Typography I",
     "Undergraduate course. Concordia University, Fall 2017.",
     "Concordia", "Courses Taught"),

    ("09/01/2016", "12/31/2016",
     "CART 253a/b Creative Computation I",
     "Undergraduate course, two sections. Concordia University, Fall 2016.",
     "Concordia", "Courses Taught"),

    ("09/01/2015", "12/31/2015",
     "CART 253a/b Creative Computation I",
     "Undergraduate course, two sections. Concordia University, Fall 2015.",
     "Concordia", "Courses Taught"),

    ("09/01/2014", "12/31/2014",
     "CART 253a/b Creative Computation I",
     "Undergraduate course, two sections. Concordia University, Fall 2014.",
     "Concordia", "Courses Taught"),

    ("01/01/2013", "04/30/2013",
     "CART 345 Computational Texts & Typography I / CART 444 Portfolio Studio",
     "Undergraduate courses. Concordia University, Winter 2013.",
     "Concordia", "Courses Taught"),

    ("09/01/2012", "12/31/2012",
     "CART 253a/b Creative Computation I",
     "Undergraduate course, two sections. Concordia University, Fall 2012.",
     "Concordia", "Courses Taught"),

    ("01/01/2012", "04/30/2012",
     "CART 345 Computational Texts & Typography I / CART 444 Portfolio Studio",
     "Undergraduate courses. Concordia University, Winter 2012.",
     "Concordia", "Courses Taught"),

    ("09/01/2011", "12/31/2011",
     "CART 253aa/a Creative Computation I/II",
     "Undergraduate course, two sections. Concordia University, Fall 2011.",
     "Concordia", "Courses Taught"),

    ("01/01/2011", "04/30/2011",
     "CART 253aa/a Creative Computation I/II",
     "Undergraduate course, two sections. Concordia University, Winter 2011.",
     "Concordia", "Courses Taught"),

    ("09/01/2010", "12/31/2010",
     "CART 345 Computational Texts & Typography I",
     "Undergraduate course. Concordia University, Fall 2010.",
     "Concordia", "Courses Taught"),

    ("01/01/2008", "04/30/2008",
     "CART 253aa/a Creative Computation I/II",
     "Undergraduate course, two sections. Concordia University, Winter 2008.",
     "Concordia", "Courses Taught"),

    ("09/01/2007", "12/31/2007",
     "DART 503 Theories of Interactivity / CART 355c Topics in Kinetic Imagery (The Next Text)",
     "Graduate and undergraduate courses. Concordia University, Fall 2007.",
     "Concordia", "Courses Taught"),

    ("01/01/2007", "04/30/2007",
     "CART 253a/b Languages of Programming",
     "Undergraduate course, two sections. Concordia University, Winter 2007.",
     "Concordia", "Courses Taught"),

    ("09/01/2006", "12/31/2006",
     "DART 503 Theories of Interactivity / CART 355c Topics in Kinetic Imagery (The Next Text)",
     "Graduate and undergraduate courses. Concordia University, Fall 2006.",
     "Concordia", "Courses Taught"),

    ("01/01/2006", "04/30/2006",
     "CART 253a/aa The Languages of Programming",
     "Undergraduate course, two sections. Concordia University, Winter 2006.",
     "Concordia", "Courses Taught"),

    ("09/01/2005", "12/31/2005",
     "CART 355b Topics in Kinetic Imagery (The Next Text) / DART 503 Theories of Interactivity",
     "Undergraduate and graduate courses. Concordia University, Fall 2005.",
     "Concordia", "Courses Taught"),

    ("01/01/2005", "04/30/2005",
     "DFAR 253a/b The Languages of Programming",
     "Undergraduate course, two sections. Concordia University, Winter 2005.",
     "Concordia", "Courses Taught"),

    ("01/01/2004", "04/30/2004",
     "DFAR 452 TriMedia Productions / DFAR 353a The Languages of Programming",
     "Undergraduate courses. Concordia University, Winter 2004.",
     "Concordia", "Courses Taught"),

    ("09/01/2003", "12/31/2003",
     "DFAR 451 Interactive Media / DFAR 498 Bending Bits",
     "Undergraduate courses. Concordia University, Fall 2003.",
     "Concordia", "Courses Taught"),

    ("01/01/2003", "04/30/2003",
     "DFAR 353a/aa The Languages of Programming",
     "Undergraduate course, two sections. Concordia University, Winter 2003.",
     "Concordia", "Courses Taught"),

    ("09/01/2002", "12/31/2002",
     "DFAR 451a/b Interactive Media",
     "Undergraduate course, two sections. Concordia University, Fall 2002.",
     "Concordia", "Courses Taught"),

    # ── SUPERVISION ────────────────────────────────────────────────────────
    # Postdoctoral Fellows
    ("01/01/2025", PRESENT,
     "Postdoctoral Fellow: Melemaikalani Moniz",
     "Postdoctoral Fellow in Abundant Soils. Concordia University.",
     "AI", "Supervision"),

    ("01/01/2024", "12/31/2026",
     "Postdoctoral Fellow: Ceyda Yolgörmez",
     "Horizon Postdoctoral Fellow in Abundant Intelligences. Concordia University.",
     "AI", "Supervision"),

    ("01/01/2019", "12/31/2021",
     "Postdoctoral Fellow: Leuli Eschraghi",
     "Horizon Postdoctoral Fellow in Indigenous Futures. Concordia University.",
     "IIF", "Supervision"),

    # Doctoral Advisees
    ("01/01/2023", PRESENT,
     "PhD Supervisor: Juliet Mackie",
     "Reconstituting Indigenous Identities through Portraiture and Storytelling. Concordia University.",
     "Concordia", "Supervision"),

    ("01/01/2021", "12/31/2024",
     "PhD Supervisor: Mel Lefebvre",
     "Healing Through Ancestral Skin Marking: Traditional Tattooing as Healing and (Re)connection for Indigenous People. Concordia University.",
     "Concordia", "Supervision"),

    ("01/01/2019", "12/31/2023",
     "PhD Co-supervisor: Jessica Barudin",
     "Re-connecting Through Women's Teachings, Language and Movement. Concordia University.",
     "Concordia", "Supervision"),

    ("01/01/2017", "12/31/2023",
     "PhD Supervisor: Suzanne Kite",
     "Lakota Epistemology, Performance Practice, and Digital Technology. Concordia University.",
     "AI", "Supervision"),

    ("01/01/2017", PRESENT,
     "PhD Secondary Supervisor: Nafisa Sarwath",
     "Indigenous knowledge, resilience and adaptive capacity. Concordia University.",
     "Concordia", "Supervision"),

    ("01/01/2016", "12/31/2021",
     "PhD Secondary Supervisor: Michelle Brown",
     "(Re)Coding Resurgence: Indigenous Digital Media Kinnections. University of Hawaii Mānoa.",
     "AbTeC", "Supervision"),

    ("01/01/2007", "12/31/2014",
     "PhD Co-supervisor: Elizabeth LaPensée",
     "Experiencing Stories: Narrative and Experience in Interactive Media. Simon Fraser University.",
     "AbTeC", "Supervision"),

    ("01/01/2008", "12/31/2012",
     "PhD Secondary Supervisor: Miao Song",
     "Experiencing Stories: Narrative and Experience in Interactive Media. Concordia University.",
     "Concordia", "Supervision"),

    ("01/01/2008", "12/31/2011",
     "PhD Secondary Supervisor: David Johnston",
     "Aesthetic Animism: Digital Poetry as Ontological Probe. Concordia University.",
     "Research", "Supervision"),

    ("01/01/2005", "12/31/2008",
     "PhD Committee Member: Rozita Naghshin",
     "Software Design as an Aesthetic Design Practice. Concordia University.",
     "Concordia", "Supervision"),

    # Masters Thesis Advisees
    ("01/01/2022", PRESENT,
     "Masters Supervisor: Vanessa Racine",
     "Anishinaabe Love: Epistemologies & Videogames. Concordia University.",
     "AbTeC", "Supervision"),

    ("01/01/2022", "12/31/2025",
     "Masters Committee: Tarcisio Cataldi Tegani",
     "Speculative Vexillology: Exploring National Identity and Imagining Afro-Brazilian Futures through Flags. Concordia University.",
     "Concordia", "Supervision"),

    ("01/01/2021", "12/31/2024",
     "Masters Supervisor: Caeleigh Lightning Long",
     "Wawêsiwîn: The Act of Dressing Up — A Research Cree-ation Project. Concordia University.",
     "AbTeC", "Supervision"),

    ("01/01/2018", "12/31/2023",
     "Masters Supervisor: Sébastien Aubin",
     "Designing Culturally Grounded Cree Syllabaries. Concordia University.",
     "AbTeC", "Supervision"),

    ("01/01/2018", "12/31/2021",
     "Masters Supervisor: Waylon Wilson",
     "Tuscarora Virtual Realities. Concordia University.",
     "AbTeC", "Supervision"),

    ("01/01/2017", "12/31/2019",
     "Masters Supervisor: Maize Longboat",
     "Haudenosaunee Storytelling via Video Games. Concordia University.",
     "AbTeC", "Supervision"),

    ("01/01/2016", "12/31/2020",
     "Masters Co-supervisor: Nicholas Gwyn Shulman",
     "Network Arts: Seeing and Making Network Organisms. Concordia University.",
     "Research", "Supervision"),

    ("01/01/2014", "12/31/2024",
     "Masters Supervisor: Morgan Kennedy",
     "Storied Indigeneity in Videogames: Post-Indian Warriors and Indie Japan. Concordia University.",
     "AbTeC", "Supervision"),

    ("01/01/2012", "12/31/2015",
     "Masters Co-supervisor: Nikolaos Chandolias",
     "KinectEcho: Gesture and Vocal Recognition in New Media, Interactive Art and Live Events. Concordia University.",
     "Research", "Supervision"),

    ("01/01/2006", "12/31/2007",
     "Masters Supervisor: Leslie Plumb",
     "Transversal Entanglements: Research-Creation and the Design Process for Inflexions. Concordia University.",
     "Research", "Supervision"),

    ("01/01/2004", "12/31/2008",
     "Masters Co-supervisor: Mia Song",
     "Computer-Assisted Interactive Documentary and Performance Arts in Illimitable Space. Concordia University.",
     "Research", "Supervision"),

    ("01/01/2003", "12/31/2005",
     "Masters Committee: Rozita Naghshin",
     "CASE Tool Simplification Via Task-Sensitive Metaphor. Concordia University.",
     "Concordia", "Supervision"),

    # ── SERVICE ────────────────────────────────────────────────────────────
    # Administrative roles
    ("01/01/2010", "12/31/2018",
     "Acting Chair",
     "Department of Design and Computation Arts, Concordia University. Various 1-to-2-week terms.",
     "Concordia", "Service"),

    ("09/01/2003", "08/31/2013",
     "Computation Arts Undergraduate Program Director / Co-director",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    ("09/01/2005", "08/31/2008",
     "Graduate Program Director",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    ("09/01/2003", "08/31/2014",
     "Computation Lab Director",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    # Departmental committees
    ("01/01/2008", "12/31/2020",
     "Personnel Committee",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    ("01/01/2002", "12/31/2014",
     "CART Curriculum Committee, Chair",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    ("01/01/2002", PRESENT,
     "Undergraduate and Graduate Admissions Committees",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    # Faculty committees
    ("01/01/2005", "12/31/2008",
     "Faculty Research Advisory Committee",
     "Faculty of Fine Arts, Concordia University.",
     "Concordia", "Service"),

    ("01/01/2005", "12/31/2008",
     "Hexagram-Concordia Steering Committee",
     "Concordia University.",
     "Concordia", "Service"),

    # University roles
    ("01/01/2020", PRESENT,
     "Co-director, Indigenous Futures Research Center",
     "Concordia University.",
     "IIF", "Service"),

    ("01/01/2020", PRESENT,
     "Indigenous Directions Leadership Council",
     "Concordia University.",
     "IIF", "Service"),

    ("01/01/2015", PRESENT,
     "Milieux Research Institute Advisory Board",
     "Concordia University.",
     "Concordia", "Service"),

    ("01/01/2015", "12/31/2018",
     "Senate Research Committee",
     "Concordia University.",
     "Concordia", "Service"),

    ("01/01/2009", "12/31/2018",
     "Board Member (Founding), Research Centre on Technoculture, Art and Gaming (TAG)",
     "Concordia University.",
     "Concordia", "Service"),

    ("01/01/2011", "12/31/2014",
     "Faculty Senate",
     "Concordia University.",
     "Concordia", "Service"),

    # External committees
    ("01/01/2025", "12/31/2028",
     "Advisory Board, Digital Technologies Research Centre",
     "National Research Council of Canada.",
     "Research", "Service"),

    ("01/01/2021", "12/31/2023",
     "Advisory Council on Artificial Intelligence",
     "Government of Canada.",
     "AI", "Service"),

    ("01/01/2020", "12/31/2022",
     "Canadian Commission for UNESCO Working Groups on AI Ethics & the Sustainable Development Goals",
     "",
     "AI", "Service"),

    ("01/01/2016", "12/31/2022",
     "Board Member, imagineNATIVE Film + Media Arts Festival",
     "",
     "AbTeC", "Service"),

    ("01/01/2010", "12/31/2016",
     "Founding Member, New Media Advisory Board, imagineNATIVE Film + Media Arts Festival",
     "",
     "AbTeC", "Service"),

    ("01/01/2006", PRESENT,
     "Co-Director, Aboriginal Territories in Cyberspace Research Network",
     "",
     "AbTeC", "Service"),

    ("01/01/2013", "12/31/2016",
     "First Peoples Literary Prize Incubating Committee & Founding Advisory Board",
     "Blue Metropolis International Literary Festival, Montreal, QC.",
     "AbTeC", "Service"),

]

def derive_cv_dimensions(rows_in):
    """Add org (institution) and program (funding agency) columns.
    - org is set only for Employment and Education rows.
    - program (agency) and project (role) are set only for Funding rows.
    - All other rows get empty strings so they appear as untagged in the filter.
    """
    early_career_orgs = [
        ('Arts Alliance Laboratory', 'Arts Alliance Laboratory'),
        ('Arts Alliance Ventures',   'Arts Alliance Ventures'),
        ('Interval Research',        'Interval Research Corporation'),
        ('Fitch',                    'Fitch, Inc.'),
        ('Lollapalooza',             "Lollapalooza '94 Tour"),
        ('Carnegie Research Fellow', 'Institute for Research on Learning'),
        ('Stanford University',      'Stanford University'),
    ]
    edu_orgs = [
        ('Royal College of Art', 'Royal College of Art'),
        ('Freie Universität',    'Freie Universität Berlin'),
        ('Stanford University',  'Stanford University'),
    ]
    # Ordered by specificity (longer/more specific first)
    agencies = [
        ('Social Sciences and Humanities Research Council', 'Social Sciences and Humanities Research Council'),
        ('Natural Sciences and Engineering Research Council','Natural Sciences and Engineering Research Council'),
        ('Canada First Research Excellence Fund',           'Canada First Research Excellence Fund'),
        ('New Frontiers in Research Fund',                  'New Frontiers in Research Fund'),
        ('Pierre Elliott Trudeau Foundation',               'Pierre Elliott Trudeau Foundation'),
        ('Fonds de recherche',                              'Fonds de recherche du Québec'),
        ('Fonds québécois',                                 'Fonds québécois de la recherche'),
        ('MacArthur Foundation',                            'The MacArthur Foundation'),
        ('Schmidt Family Foundation',                       'Schmidt Family Foundation'),
        ('Canada Foundation for Innovation',                'Canada Foundation for Innovation'),
        ('Canada Council for the Arts',                     'Canada Council for the Arts'),
        ('Hexagram Institute',                              'Hexagram Institute'),
        ('Heritage Canada',                                 'Heritage Canada'),
        ('Hewitt Foundation',                               'Hewitt Foundation'),
        ('Kanaeokana Network',                              'Kanaeokana Network'),
        ('Indigenous Screen Office',                        'Indigenous Screen Office'),
        ('Arts Council of England',                         'Arts Council of England'),
        ('McConnell Family Foundation',                     'J. W. McConnell Family Foundation'),
        ('Montalvo Arts Center',                            'Montalvo Arts Center'),
        ('Fine Arts-Engineering Seed Grants',               'Concordia Fine Arts-Engineering'),
        ('Fine Arts Faculty',                               'Concordia Fine Arts Faculty'),
        ('Office of Research',                              'Concordia Office of Research'),
        ('Jarislowsky Institute',                           'Jarislowsky Institute'),
        ('Concordia University',                            'Concordia University'),
    ]

    result = []
    for row in rows_in:
        start, end, headline, desc, _project, group = row[:6]
        org = ''
        program = ''
        role = ''

        if group == 'Education':
            for keyword, institution in edu_orgs:
                if keyword in headline:
                    org = institution
                    break

        elif group == 'Employment':
            org = 'Concordia University'  # default; overridden for pre-Concordia
            for keyword, institution in early_career_orgs:
                if keyword in headline:
                    org = institution
                    break

        elif group in ('Funding (PI)', 'Funding (Co-I)', 'Funding (Internal)'):
            for keyword, agency in agencies:
                if keyword in desc:
                    program = agency
                    break
            if group == 'Funding (PI)':
                if 'Artist.' in desc:
                    role = 'Artist'
                elif 'Research Director' in desc:
                    role = 'Research Director'
                elif 'Fellow' in headline:
                    role = 'Fellow'
                elif 'Co-lead' in desc:
                    role = 'Co-lead'
                elif 'Co-grant holder' in desc:
                    role = 'Co-grant Holder'
                else:
                    role = 'Primary Investigator'
            elif group == 'Funding (Co-I)':
                role = 'Core Applicant' if 'Core Applicant' in desc else 'Co-investigator'
            else:  # Funding (Internal)
                role = 'Internal'

        result.append((start, end, headline, desc, role, group, org, program))
    return result


rows = derive_cv_dimensions(rows)
rows.sort(key=lambda r: GRP_ORDER.index(r[5]) if r[5] in GRP_ORDER else 99)

for row in rows:
    ws.append(list(row))

# Auto-width columns
for col in ws.columns:
    max_len = max(len(str(cell.value or "")) for cell in col)
    ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 60)

path = Path(__file__).parent / "cv.xlsx"
wb.save(path)
print(f"Saved {len(rows)} rows to {path}")
