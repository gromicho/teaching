# Lecture 1 graphic attribution register

This register covers every graphic in the native Beamer Lecture 1 deck.
It complements the slide-level source lines and hyperlinks.  It distinguishes a
**source link** from a **reuse permission**: a source link helps students find
current evidence; it does not by itself license the image.

## How to use the register

- `Verified/current`: the slide contains a direct link to the named primary or
  maintained source.
- `Institutional/course`: the graphic is a UvA/ABW mark or a native course
  illustration.
- `Inherited—pending`: extracted from the original PowerPoint, but the original
  deck did not record a creator, licence or permitted reuse. It is retained for
  the legacy course deck only pending a rights record.
- Individual PowerPoint object provenance is in
  `assets/visuals/lecture-1/manifest.json`; this register gives the
  presentation-level interpretation.

| Deck visual family | Status and visible source / attribution |
|---|---|
| UvA crest and ABW logo | Institutional/course asset. |
| Amsterdam canal title image | Inherited—pending creator and reuse record. |
| Staff portraits and former-activity logos | Inherited personnel/institutional assets; photographer, logo permissions and usage basis to be recorded before public reuse. |
| INFORMS definition and logo | [INFORMS Operations Research & Analytics](https://www.informs.org/Explore/Operations-Research-Analytics). |
| Gartner model | [Gartner Data and Analytics](https://www.gartner.com/en/topics/data-and-analytics); third-party teaching figure. |
| COVID descriptive data | [Our World in Data COVID-19](https://ourworldindata.org/coronavirus); historical chart. |
| Seasonal-flu diagnostic chart | [RAND (2011), Figure 2](https://www.rand.org/content/dam/rand/pubs/research_briefs/2011/RAND_RB9572.pdf); redrawn. |
| COVID prediction scenario | [EpiRisk](https://epirisk.net/); historical scenario. |
| COVID prescription figure | [Bertsimas et al. (2020)](https://doi.org/10.1007/s10729-020-09542-0). |
| Calculator product image | Inherited—pending product-image source/reuse record; calculator rule links to SEFA. |
| Big Data montage | Inherited—pending creators/rights. Current contexts link to [Our World in Data](https://ourworldindata.org/grapher/historical-cost-of-computer-memory-and-storage) and the [MO-book TSP notebook](https://mobook.github.io/MO-book/notebooks/04/08-traveling-salesman-problem.html). |
| LHC and Walmart images | LHC: [CERN/ATLAS](https://atlas-public.web.cern.ch/updates/briefing/run-3-trigger). Walmart image/rate: inherited—pending. |
| Internet-minute infographic | [eDiscovery Today and LTMG](https://ediscoverytoday.com/2023/04/20/2023-internet-minute-infographic-by-ediscovery-today-and-ltmg-ediscovery-trends/); historical estimate. |
| IoT, storage and Moore's-law charts | [IoT Analytics](https://iot-analytics.com/number-connected-iot-devices/), [Our World in Data storage](https://ourworldindata.org/grapher/historical-cost-of-computer-memory-and-storage), and [Our World in Data transistors](https://ourworldindata.org/grapher/transistors-per-microprocessor). |
| TSP figures and history | [University of Waterloo TSP project](https://www.math.uwaterloo.ca/tsp/) and [MO-book TSP notebook](https://mobook.github.io/MO-book/notebooks/04/08-traveling-salesman-problem.html). |
| SDG icons | [United Nations SDG materials](https://www.un.org/sustainabledevelopment/news/communications-material/). |
| Dike case | [Eijgenraam et al. (2012)](https://doi.org/10.1287/opre.1110.1028); inherited photos pending. |
| Hunger / WFP case | [World Food Programme supply chain](https://www.wfp.org/supply-chain); inherited photos pending. |
| Timor-Leste case | [Maintained teaching notebook](https://github.com/gromicho/teaching/blob/main/foundations/cases/timor-leste-preparation.ipynb); inherited context photographs pending. |
| FeedCalculator app, map, farmer and workshop images | [FeedCalculator](https://www.feedcalculator.org/) for the current project information; inherited images pending individual source/rights record. |
| Python, Jupyter, Colab and CodeGrade marks or interface references | [Python trademark policy](https://www.python.org/psf/trademarks/), [Project Jupyter](https://jupyter.org/), [Google Colab](https://colab.research.google.com/), and [CodeGrade student guide](https://help.codegrade.com/for-students/getting-started/getting-started-in-codegrade). |
| AI coach and human-directs-AI artwork | Project-generated conceptual illustrations, August 2026; not documentary images. |
| AF447 factual sequence | [BEA investigation](https://bea.aero/en/investigation-reports/notified-events/detail/accident-to-the-airbus-a330-203-registered-f-gzcp-and-operated-by-air-france-occured-on-06-01-2009-in-the-atlantic-ocean). |

## Asset-level record

The original deck supplied 101 separately extracted graphic objects. Every one
is named and traced in `assets/visuals/lecture-1/manifest.json` with original
PowerPoint slide, object name, current filename, and attribution status. Items
with `needs-rights-review` must not be represented as open or course-owned art.
