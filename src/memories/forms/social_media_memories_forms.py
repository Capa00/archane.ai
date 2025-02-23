from django import forms


class LTM(forms.Form):
    OBJECTIVES_HELP_TEXT = """
        Examples: <br>
        * Increase brand awareness <br>
        * Generate qualified leads for conversion <br>
        * Boost online sales by 20% in the next 6 months <br>
        * Improve customer retention rates <br>
        <br>
        """
    objectives = forms.CharField(help_text=OBJECTIVES_HELP_TEXT, widget=forms.Textarea(), required=False)

    TARGET_AUDIENCE_HELP_TEXT = """
        Examples: <br>
        * Women aged 25 to 40 interested in wellness and fashion <br>
        * Young professionals enthusiastic about innovative technologies <br>
        * Families seeking eco-friendly products <br>
        * Sports and fitness enthusiasts <br>
        <br>
        """
    target_audience = forms.CharField(help_text=TARGET_AUDIENCE_HELP_TEXT, widget=forms.Textarea(), required=False)

    BRAND_IDENTITY_HELP_TEXT = """
        Examples: <br>
        * A youthful, dynamic, and innovative brand <br>
        * A friendly, informal, and transparent tone of voice <br>
        * Values centered around sustainability and innovation <br>
        * A professional and reliable image <br>
        <br>
        """
    brand_identity = forms.CharField(help_text=BRAND_IDENTITY_HELP_TEXT, widget=forms.Textarea(), required=False)

    CURRENT_STATUS_HELP_TEXT = """
        Examples: <br>
        * Active on Facebook, Instagram, and LinkedIn <br>
        * Strong community engagement on Instagram but low on LinkedIn <br>
        * Primarily visual content (photos and videos) with inconsistent results <br>
        * Regular posting without an integrated content strategy <br>
        <br>
        """
    current_status = forms.CharField(help_text=CURRENT_STATUS_HELP_TEXT, widget=forms.Textarea(), required=False)

    BUDGET_RESOURCES_HELP_TEXT = """
        Examples: <br>
        * Monthly budget of approximately €1,500 for sponsored campaigns and content creation <br>
        * An in-house team consisting of a social media manager and a content creator <br>
        * Possibility to collaborate with freelancers or external agencies <br>
        * Limited video production resources but strong photographic capabilities <br>
        """
    budget_resources = forms.CharField(help_text=BUDGET_RESOURCES_HELP_TEXT, widget=forms.Textarea(), required=False)

    CONTENT_HELP_TEXT = """
        Examples: <br>
        * Video tutorials and live streams demonstrating product usage <br>
        * High-quality photo posts and interactive Instagram stories <br>
        * In-depth blog articles and infographics on the company website <br>
        * User-generated content to boost engagement <br>
        <br>
        """
    content = forms.CharField(help_text=CONTENT_HELP_TEXT, widget=forms.Textarea(), required=False)

    COMPETITORS_HELP_TEXT = """
        Examples: <br>
        * Brand X: Strong Instagram presence with a focus on visual storytelling <br>
        * Brand Y: Intensive use of influencer marketing <br>
        * Brand Z: Recurring promotional campaigns on Facebook and LinkedIn <br>
        * Local competitors offering similar services with less digital emphasis <br>
        <br>
        """
    competitors = forms.CharField(help_text=COMPETITORS_HELP_TEXT, widget=forms.Textarea(), required=False)

    MEASURING_SUCCESS_HELP_TEXT = """
        Examples: <br>
        * Monitoring engagement rate (likes, comments, shares) <br>
        * Growth in followers and increased website traffic <br>
        * Conversions tracked via sponsored campaigns <br>
        * Analysis of lead generation metrics and campaign ROI <br>
        <br>
        """
    measuring_success = forms.CharField(help_text=MEASURING_SUCCESS_HELP_TEXT, widget=forms.Textarea(), required=False)

    FUTURE_CAMPAIGNS_HELP_TEXT = """
        Examples: <br>
        * Launching a new product in the next quarter <br>
        * Promotional campaign aligned with seasonal holidays (e.g., Christmas or Easter) <br>
        * Collaborations with influencers to enhance visibility <br>
        * Online contests to encourage engagement and content sharing <br>
        <br>
        """
    future_campaigns = forms.CharField(help_text=FUTURE_CAMPAIGNS_HELP_TEXT, widget=forms.Textarea(), required=False)

    CRISIS_MANAGEMENT_HELP_TEXT = """
        Examples: <br>
        * A protocol to respond to negative comments within 24 hours <br>
        * An internal communication plan for addressing critical feedback <br>
        * A monitoring strategy to anticipate potential crises on social media <br>
        * Predefined guidelines for the team on handling emergency situations <br>
        <br>
        """
    crisis_management = forms.CharField(help_text=CRISIS_MANAGEMENT_HELP_TEXT, widget=forms.Textarea(), required=False)
