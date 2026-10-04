/* ============================================================
   Pack 1125 site configuration — single source of truth.
   Plain static JS (no modules, no build step). Loaded on
   every page via <script src="config.js"></script>.

   A future editor can update pack facts here. Some copy is
   still inline in the HTML pages; keep both in sync when
   facts change.
   ============================================================ */

const CONFIG = {
  pack: {
    number: "1125",
    name: "Cub Scout Pack 1125",
    tagline: "Leaders and Trailblazers",
    location: "Dumfries, Virginia",
    founded: "November 2025",
    serves: [
      "Covington-Harper Elementary School",
      "Swans Creek Elementary School",
      "Triangle Elementary School",
      "Leesylvania Elementary School"
    ],
    note: "Secular pack — open to both boys and girls",
    pillars: [
      "Leadership & Trailblazing",
      "Character",
      "Core Values",
      "Honor"
    ]
  },

  charter: {
    org: "Future Kings, Inc.",
    note: "Dumfries-based nonprofit organization dedicated to youth leadership, character development, and positive community impact"
  },

  council: {
    name: "National Capital Area Council",
    short: "NCAC",
    org: "Scouting America",
    url: "https://ncacscouting.org",
    district: "Prince William District"
  },

  leaders: [
    { role: "Cubmaster", name: "Clive Vella" },
    { role: "Committee Chair", name: "Dr. Neville Welch" },
    { role: "Website & Technical Support", name: "Brandon Rogers" },
    // Open: den leaders and committee members (recruiting as of Oct 2026)
  ],

  meeting: {
    packMeeting: "1st Thursday",
    denMeeting: "3rd Thursday",
    time: "6:30–7:30 PM",
    season: "October–January",
    venue: "Covington-Harper Elementary School auditorium",
    town: "Dumfries VA"
    // NOTE: venue may change — keep the address as school name + Dumfries VA only.
  },

  contact: {
    email: "admin@pack1125.org",
    // Cubmaster phone removed from the public site (Oct 2026); families reach Clive via the pack email.
    myScouting: "https://my.scouting.org/create-account",
    financialAid: "https://ncacscouting.org/resources/financial-support/",
    financialAidForm: "https://247scouting.com/forms/082-FinancialSupport2026v2",
    beAScout: "https://beascout.scouting.org", // TBD: replace with the pack's own pin link
    scoutbook: "https://advancements.scouting.org"
  },

  dues: {
    perScoutPerYear: null, // TBA for this year
    display: "To be announced",
    national: 85,   // Scouting America registration fee
    ncac: 80,       // NCAC participation fee — first-year Cub Scouts only
    adult: 65,      // reduced adult registration fee
    note: "Financial aid available — NCAC First-Year Full Financial Support Program"
  },

  program: {
    ranks: ["Lion", "Tiger", "Wolf", "Bear", "Webelos", "Arrow of Light"],
    grades: "K–5",
    welcome: "Boys and girls welcome",
    firstAchievement: "Bobcat",
    motto: "Do Your Best"
  },

  activities: [
    { name: "Trick or Treat", when: "October 31, 2026 (location TBD)" },
    { name: "Pack Meeting (Bottle Rocket STEM)", when: "November 5, 2026" },
    { name: "Holiday Potluck — Covington-Harper ES", when: "December 17, 2026" },
    { name: "Spring Overnight Campout — Camp Snyder", when: "May 14–16, 2027" },
    { name: "Fall Camp Day — Prince William Forest Park", when: "October 3, 2026 (held)" }
  ],

  calendar: {
    calendarId: "fa3adffd31279defe6498a672b5065eadfd8a49e248434efa24b5cd62d8e7af9@group.calendar.google.com",
    embedUrl: "https://calendar.google.com/calendar/embed?src=fa3adffd31279defe6498a672b5065eadfd8a49e248434efa24b5cd62d8e7af9%40group.calendar.google.com&ctz=America%2FNew_York"
  }
};

/* Mobile nav toggle — shared by every page's header. */
(function () {
  document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".site-nav");
    if (!toggle || !nav) return;
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
})();
