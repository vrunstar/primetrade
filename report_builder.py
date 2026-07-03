"""
report_builder.py
Builds the final PDF report using reportlab, pulling in the charts generated
by plots.py. Run after main.py (or this will generate charts itself if missing).
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, PageBreak, HRFlowable,
                                 KeepTogether)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas as pdfcanvas

from data_loader import load_merged

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
DEFAULT_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "sentiment_trader_report.pdf")
OUTPUT_PATH = os.environ.get("REPORT_OUTPUT_PATH", DEFAULT_OUTPUT_PATH)

styles = getSampleStyleSheet()

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
ACCENT = colors.HexColor("#0E6B4F")        # deep emerald - primary accent
ACCENT_DARK = colors.HexColor("#0A4E3A")   # darker emerald for headers/rules
ACCENT_SOFT = colors.HexColor("#E7F3EF")   # pale emerald tint for bands/callouts
DARK = colors.HexColor("#1B2631")          # near-black body text
GREY = colors.HexColor("#6B7A85")          # secondary/caption text
GREY_LINE = colors.HexColor("#DDE3E6")     # hairlines / table grid
GOLD = colors.HexColor("#B08D2A")          # small warm accent for emphasis marks
TABLE_HEAD = colors.HexColor("#12293B")    # navy-charcoal table header
ROW_ALT = colors.HexColor("#F6F8F7")

PAGE_W, PAGE_H = letter

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
kicker_style = ParagraphStyle(
    "Kicker", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9.5,
    textColor=ACCENT, spaceAfter=10, tracking=1,
)
title_style = ParagraphStyle(
    "TitleX", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=27,
    leading=32, textColor=DARK, spaceAfter=8, alignment=TA_LEFT,
)
subtitle_style = ParagraphStyle(
    "Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=12.5,
    leading=17, textColor=GREY, spaceAfter=22, alignment=TA_LEFT,
)
h1 = ParagraphStyle(
    "H1X", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=14.5,
    textColor=ACCENT_DARK, spaceBefore=20, spaceAfter=9, leading=18,
)
body = ParagraphStyle(
    "BodyX", parent=styles["Normal"], fontName="Helvetica", fontSize=10,
    leading=15.5, spaceAfter=8, textColor=DARK, alignment=TA_LEFT,
)
bullet = ParagraphStyle(
    "BulletX", parent=body, leftIndent=16, bulletIndent=4, spaceAfter=7, leading=15,
)
caption = ParagraphStyle(
    "Caption", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=8.5,
    textColor=GREY, alignment=TA_CENTER, spaceAfter=16, spaceBefore=6,
)
link_body = ParagraphStyle(
    "LinkBody", parent=body, fontSize=9.5, leading=14, spaceAfter=5,
    textColor=DARK,
)
footer_note = ParagraphStyle(
    "FooterNote", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=8,
    textColor=GREY, alignment=TA_LEFT, leading=12,
)
LINK_COLOR = "#0E6B4F"


def chart(name, width=6.3, height=2.42):
    return Image(os.path.join(CHARTS_DIR, name), width=width * inch, height=height * inch)


def section_header(number, text):
    """Heading with a thin emerald-toned rule underneath for visual separation."""
    return KeepTogether([
        Paragraph(text, h1),
        HRFlowable(width="100%", thickness=0.75, color=GREY_LINE, spaceAfter=10),
    ])


def build_summary_table():
    data = [
        ["Sentiment", "Trades", "Calendar Days", "Avg PnL/Trade", "Win Rate"],
        ["Extreme Fear", "21,400", "14", "$34.54", "76.2%"],
        ["Fear", "61,837", "91", "$54.29", "87.3%"],
        ["Neutral", "37,686", "67", "$34.31", "82.4%"],
        ["Greed", "50,303", "193", "$42.74", "76.9%"],
        ["Extreme Greed", "39,992", "114", "$67.89", "89.2%"],
    ]
    t = Table(data, colWidths=[1.3 * inch, 0.9 * inch, 1.1 * inch, 1.2 * inch, 0.9 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("LINEBELOW", (0, 0), (-1, 0), 1, TABLE_HEAD),
        ("LINEBELOW", (0, -1), (-1, -1), 1, GREY_LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, GREY_LINE),
        ("BOX", (0, 0), (-1, -1), 0.75, GREY_LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (4, 1), (4, -1), ACCENT_DARK),
        ("FONTNAME", (4, 1), (4, -1), "Helvetica-Bold"),
    ]))
    return t


def build_story():
    story = []

    # -------------------- Cover --------------------
    story.append(Spacer(1, 130))
    story.append(HRFlowable(width="18%", thickness=2.4, color=ACCENT, spaceAfter=14, hAlign="LEFT"))
    story.append(Paragraph("MARKET BEHAVIOR RESEARCH", kicker_style))
    story.append(Paragraph("Trader Performance vs. Bitcoin Market Sentiment", title_style))
    story.append(Paragraph("An analysis of Hyperliquid trading behavior across Fear &amp; Greed regimes", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=22))
    story.append(Paragraph(
        f'<link href="https://raw.githubusercontent.com/vrunstar/primetrade/refs/heads/main/data/fear_greed_index.csv" color="{LINK_COLOR}">'
        '<b>Dataset 1</b> &nbsp;&mdash;&nbsp; Bitcoin Fear &amp; Greed Index (Feb 2018 &ndash; May 2025)</link>',
        link_body))
    story.append(Paragraph(
        f'<link href="https://raw.githubusercontent.com/vrunstar/primetrade/refs/heads/main/data/historical_data.csv" color="{LINK_COLOR}">'
        '<b>Dataset 2</b> &nbsp;&mdash;&nbsp; Hyperliquid Historical Trade Data (May 2023 &ndash; May 2025)</link>',
        link_body))
    story.append(Spacer(1, 34))

    story.append(section_header("01", "Executive Summary"))
    story.append(Paragraph(
        "This report examines whether Bitcoin market sentiment (Fear/Greed) is associated with differences in "
        "trader performance on Hyperliquid. The headline finding is counter to the popular \"buy fear, sell greed\" "
        "heuristic at the aggregate level &mdash; <b>Extreme Greed is the most profitable and highest win-rate regime overall</b>. "
        "But the more actionable insight is behavioral: top-performing traders systematically sell into Extreme Greed while "
        "bottom-performing traders buy into Greed, and this divergence in behavior &mdash; not sentiment alone &mdash; is what "
        "separates profitable accounts from unprofitable ones.",
        body))
    story.append(PageBreak())

    story.append(section_header("02", "Data &amp; Methodology"))
    story.append(Paragraph(
        "Trade-level records from Hyperliquid were joined to the daily Bitcoin Fear &amp; Greed Index classification "
        "(Extreme Fear, Fear, Neutral, Greed, Extreme Greed) by calendar date. Of 211,225 trade rows, all but 6 matched "
        "a sentiment label &mdash; a 99.997% match rate. <b>Closed PnL</b> is realized profit/loss booked when a position "
        "is closed; most trade rows are position-building entries with Closed PnL of zero, so PnL-based metrics are "
        "computed only on the 104,402 trades that actually closed a position.",
        body))
    story.append(Spacer(1, 4))
    story.append(build_summary_table())
    story.append(Spacer(1, 12))

    story.append(section_header("03", "Performance by Market Sentiment"))
    story.append(Paragraph(
        "Average PnL per trade and win rate both peak in Extreme Greed and are weakest in Neutral and Extreme Fear. "
        "This runs counter to a naive contrarian assumption that fear is the best time to be trading profitably &mdash; "
        "in this dataset, momentum into strength was, on average, the more rewarded regime.",
        body))
    story.append(chart("01_pnl_winrate.png"))
    story.append(Paragraph("Figure 1. Average Closed PnL per trade and win rate across sentiment regimes.", caption))

    story.append(section_header("04", "Distribution of Outcomes, Not Just Averages"))
    story.append(Paragraph(
        "Averages can hide spread. Looking at the full distribution of per-trade PnL (clipped to the 2nd-98th "
        "percentile to control for outliers), Extreme Greed and Fear show tighter, more positively-skewed "
        "distributions, while Extreme Fear and Neutral show wider spreads with more downside outliers.",
        body))
    story.append(chart("07_pnl_distribution.png", width=5.6, height=2.8))
    story.append(Paragraph("Figure 2. Boxplot of Closed PnL per trade by sentiment regime.", caption))
    story.append(PageBreak())

    story.append(section_header("05", "Trading Activity by Sentiment"))
    story.append(Paragraph(
        "Normalizing by the number of calendar days in each regime reveals that trading intensity &mdash; both trade "
        "frequency and dollar volume &mdash; is far higher during Extreme Fear than any other regime, consistent with "
        "panic-driven activity and capitulation events. Note Extreme Fear spans only 14 days in this window, so this "
        "result should be treated as directional rather than statistically robust.",
        body))
    story.append(chart("02_activity.png"))
    story.append(Paragraph("Figure 3. Trades per day and volume per day, normalized by calendar days per regime.", caption))

    story.append(section_header("06", "Position Sizing by Sentiment"))
    story.append(Paragraph(
        "Trade size (USD) also varies by regime. Traders place their largest average trades during Fear and Greed, "
        "and noticeably smaller trades during Extreme Greed &mdash; consistent with a distribution/de-risking pattern "
        "as euphoria peaks rather than sizing up further.",
        body))
    story.append(chart("08_trade_size_distribution.png", width=5.6, height=2.8))
    story.append(Paragraph("Figure 4. Boxplot of trade size (USD) by sentiment regime.", caption))
    story.append(PageBreak())

    story.append(section_header("07", "Does Skill Matter More in Certain Regimes?"))
    story.append(Paragraph(
        "Accounts were ranked by total realized PnL; the top 8 and bottom 8 accounts were compared across sentiment "
        "regimes. The performance gap between skilled and unskilled traders widens sharply in Greed and Extreme Greed &mdash; "
        "top traders' average PnL per trade climbs to over $170 in Extreme Greed, while bottom traders' average PnL "
        "turns negative in both Greed (-$50.84) and Extreme Fear (-$22.58).",
        body))
    story.append(chart("03_top_vs_bottom_pnl.png", width=5.6, height=2.55))
    story.append(Paragraph("Figure 5. Average PnL per trade, top 8 vs. bottom 8 accounts by total realized PnL.", caption))

    story.append(section_header("08", "The Key Behavioral Divide: Who Sells the Top?"))
    story.append(Paragraph(
        "This is the strongest and most actionable signal in the dataset. As sentiment moves into Extreme Greed, "
        "top-performing accounts shift decisively toward <b>selling</b> &mdash; about 67% of their trades are sells, up "
        "from roughly parity in calmer regimes. Bottom-performing accounts move the opposite way: their buy share "
        "rises to about 56% during Greed, meaning they are on average accumulating positions right as the top "
        "performers are distributing into strength.",
        body))
    story.append(chart("04_buysell_bias.png"))
    story.append(Paragraph("Figure 6. Buy/sell composition by sentiment regime, top vs. bottom traders.", caption))
    story.append(PageBreak())

    story.append(section_header("09", "Account-Level View: Volume, PnL, and Win Rate"))
    story.append(Paragraph(
        "Plotting each account's total volume against its total realized PnL (bubble size = trade count, color = win "
        "rate) shows that high volume alone doesn't guarantee profitability &mdash; several high-volume accounts cluster "
        "near breakeven or negative, while some of the most profitable accounts operate at moderate volume with high "
        "win rates.",
        body))
    story.append(chart("10_account_scatter.png", width=5.4, height=3.24))
    story.append(Paragraph("Figure 7. Account-level total volume vs. total PnL, sized by trade count, colored by win rate.", caption))

    story.append(section_header("10", "Sentiment vs. Aggregate PnL Over Time"))
    story.append(Paragraph(
        "Plotting the daily sentiment index value against a 7-day rolling average of aggregate daily Closed PnL shows "
        "no strong linear relationship &mdash; the direct correlation between same-day sentiment value and aggregate PnL "
        "is approximately -0.08. Sentiment functions better as a behavioral segmentation variable (Sections 6-7) than "
        "as a standalone predictive signal for next-period returns.",
        body))
    story.append(chart("05_timeline.png"))
    story.append(Paragraph("Figure 8. Fear &amp; Greed Index value (left axis) vs. 7-day average daily Closed PnL (right axis).", caption))
    story.append(PageBreak())

    story.append(section_header("11", "Cumulative Performance Across Regimes"))
    story.append(Paragraph(
        "Tracking cumulative aggregate PnL over the full period, shaded by the prevailing sentiment regime at each "
        "point in time, shows that gains accrue in bursts rather than smoothly, with several of the steepest climbs "
        "occurring during Fear and Extreme Greed periods rather than calmer Neutral stretches.",
        body))
    story.append(chart("09_cumulative_pnl.png"))
    story.append(Paragraph("Figure 9. Cumulative Closed PnL over time, background shaded by sentiment regime.", caption))

    story.append(section_header("12", "Market Composition"))
    story.append(Paragraph(
        "BTC dominates traded volume at roughly $644M, more than 4x the next largest asset (HYPE at $142M), followed "
        "by SOL and ETH. Sentiment-driven behavioral patterns above are therefore substantially, though not exclusively, "
        "a BTC-driven effect given the dataset's concentration.",
        body))
    story.append(chart("06_top_coins.png", width=5.0, height=2.78))
    story.append(Paragraph("Figure 10. Top 8 traded coins by total volume (USD).", caption))
    story.append(PageBreak())

    story.append(section_header("13", "PnL by Coin and Sentiment Regime"))
    story.append(Paragraph(
        "Breaking down average PnL per trade by both coin and sentiment regime shows the Extreme Greed effect is not "
        "uniform &mdash; it is strongest in BTC and SOL, while other majors show more mixed results across regimes, "
        "reinforcing that regime effects are asset-dependent rather than purely a market-wide phenomenon.",
        body))
    story.append(chart("11_coin_sentiment_heatmap.png", width=5.0, height=3.06))
    story.append(Paragraph("Figure 11. Average Closed PnL per trade, top 6 coins x sentiment regime.", caption))

    story.append(section_header("14", "Extreme Fear vs. Extreme Greed: Head to Head"))
    story.append(Paragraph(
        "Overlaying the PnL distributions for the two extreme regimes directly shows Extreme Greed's distribution "
        "is shifted further right (more mass in positive territory) than Extreme Fear's, visually confirming the "
        "difference in average outcomes seen in Section 2.",
        body))
    story.append(chart("12_extreme_regime_hist.png", width=5.4, height=2.97))
    story.append(Paragraph("Figure 12. Overlaid PnL distributions for Extreme Fear vs. Extreme Greed.", caption))
    story.append(PageBreak())

    story.append(section_header("15", "Fee Impact by Sentiment"))
    story.append(Paragraph(
        "Fees represent a larger relative drag on returns during Extreme Fear and Neutral regimes, where gross PnL "
        "per trade is thinner. In Extreme Greed, where gross edge is strongest, fees are a smaller proportional cost. "
        "This implies execution efficiency (fee minimization, avoiding overtrading) matters most precisely when the "
        "underlying edge is weakest.",
        body))

    story.append(section_header("16", "Key Findings"))
    findings = [
        "<b>Extreme Greed is the most profitable and highest win-rate regime overall</b> &mdash; average PnL per trade "
        "(~$68) and win rate (~89%) both peak here, contradicting the naive \"buy fear, sell greed\" assumption at the aggregate level.",
        "<b>Skill separates hardest in Greed/Extreme Greed.</b> Top traders' edge over bottom traders is largest exactly "
        "when the crowd is most euphoric.",
        "<b>The defining behavioral split is who sells the top.</b> Top traders shift decisively toward selling (~67%) "
        "as Extreme Greed builds; bottom traders shift toward buying (~56%) into Greed &mdash; chasing the move top traders are exiting.",
        "<b>High volume does not guarantee profitability</b> at the account level &mdash; win rate and trade selectivity "
        "matter more than raw activity.",
        "<b>Regime effects are asset-dependent</b>, strongest in BTC and SOL among top-traded coins.",
        "<b>Extreme Fear sees the highest daily trading intensity</b>, consistent with panic-driven activity and "
        "capitulation &mdash; though based on a small 14-day sample in this window.",
        "<b>Sentiment is not a strong standalone linear predictor of daily PnL</b> (correlation &asymp; -0.08). Its value "
        "is as a segmentation variable for behavior and skill, not as a direct signal.",
        "<b>Fees bite hardest, relatively, in Fear/Neutral regimes</b> where gross edge is thinner.",
    ]
    for f in findings:
        story.append(Paragraph("&#9642;&nbsp; " + f, bullet))

    story.append(section_header("17", "Strategy Implications"))
    implications = [
        "<b>Use sentiment as a position-sizing and discipline filter, not a standalone entry signal.</b> The raw "
        "correlation is weak, but skilled traders systematically behave differently by regime, and that behavior "
        "correlates with performance.",
        "<b>Build explicit profit-taking triggers keyed to Extreme Greed.</b> Top-performing accounts are structurally "
        "selling into strength here; a rules-based scale-out mirrors profitable trader behavior.",
        "<b>Be skeptical of new buying activity during Greed.</b> This is where bottom-quartile traders concentrate "
        "their losses &mdash; a good regime to tighten risk limits or require stronger confirmation before adding longs.",
        "<b>Favor selectivity over volume.</b> The account-level view shows raw activity doesn't correlate with "
        "profitability; win rate and trade quality do.",
        "<b>Expect a spike in activity during Extreme Fear</b>, but size conservatively given the small historical "
        "sample and higher variance of outcomes in that regime.",
        "<b>Watch fee drag in Fear/Neutral conditions</b>; thinner edges make execution costs proportionally more damaging.",
    ]
    for i in implications:
        story.append(Paragraph("&#9642;&nbsp; " + i, bullet))

    story.append(Spacer(1, 22))
    story.append(HRFlowable(width="100%", thickness=0.75, color=GREY_LINE, spaceAfter=10))
    story.append(Paragraph(
        "Analysis based on Hyperliquid historical trade data (211,225 trades, 32 accounts, May 2023 &ndash; May 2025) "
        "merged with the Bitcoin Fear &amp; Greed Index by calendar date. Full code and reproducible analysis available "
        "in the accompanying Python scripts (data_loader.py, metrics.py, plots.py, main.py, report_builder.py).",
        footer_note))

    return story


# ---------------------------------------------------------------------------
# Page furniture: header rule + footer with page numbers, skipped on cover
# ---------------------------------------------------------------------------
class NumberedCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if total_pages > 1 and self._pageNumber > 1:
                self._draw_furniture(total_pages)
            self._pageNumber_super_showPage()
        pdfcanvas.Canvas.save(self)

    def _pageNumber_super_showPage(self):
        pdfcanvas.Canvas.showPage(self)

    def _draw_furniture(self, total_pages):
        self.saveState()
        # top hairline + running title
        self.setStrokeColor(GREY_LINE)
        self.setLineWidth(0.5)
        self.line(0.75 * inch, PAGE_H - 0.55 * inch, PAGE_W - 0.75 * inch, PAGE_H - 0.55 * inch)
        self.setFont("Helvetica", 8)
        self.setFillColor(GREY)
        self.drawString(0.75 * inch, PAGE_H - 0.48 * inch,
                         "Trader Performance vs. Bitcoin Market Sentiment")
        self.drawRightString(PAGE_W - 0.75 * inch, PAGE_H - 0.48 * inch, "Hyperliquid Research")
        # bottom hairline + page number
        self.setStrokeColor(GREY_LINE)
        self.line(0.75 * inch, 0.55 * inch, PAGE_W - 0.75 * inch, 0.55 * inch)
        self.setFont("Helvetica", 8)
        self.setFillColor(GREY)
        self.drawCentredString(PAGE_W / 2.0, 0.38 * inch,
                                f"{self._pageNumber} / {total_pages}")
        self.restoreState()


def build_report():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter,
                             topMargin=0.85 * inch, bottomMargin=0.8 * inch,
                             leftMargin=0.75 * inch, rightMargin=0.75 * inch)
    doc.build(build_story(), canvasmaker=NumberedCanvas)
    print(f"PDF written to {OUTPUT_PATH}")


if __name__ == "__main__":
    if not os.path.isdir(CHARTS_DIR) or len(os.listdir(CHARTS_DIR)) < 12:
        print("Charts missing, generating first...")
        from plots import generate_all
        merged, sentiment, trades = load_merged(verbose=False)
        generate_all(merged, sentiment)
    build_report()