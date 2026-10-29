from pathlib import Path
import unittest


HTML = Path(__file__).resolve().parents[1] / "index.html"


class LiveDataContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML.read_text(encoding="utf-8")

    def test_dashboard_does_not_seed_fake_company_or_stream_data(self):
        self.assertFalse("seedCompanies" in self.html, "seed company data remains")
        self.assertFalse("streamTemplates" in self.html, "simulated event data remains")
        self.assertFalse("Math.random()" in self.html, "random chart data remains")

    def test_exchange_rates_use_the_real_public_frankfurter_api(self):
        self.assertTrue("https://api.frankfurter.dev/v2/rates" in self.html, "missing live FX provider")
        self.assertTrue("base=USD" in self.html, "missing USD base currency")

    def test_business_dashboard_reads_from_a_same_origin_backend(self):
        self.assertTrue("/api/companies" in self.html, "missing companies backend route")
        self.assertTrue("/api/analytics/summary" in self.html, "missing analytics backend route")

    def test_no_project_is_created_without_real_company_data(self):
        self.assertTrue("sourceUnavailable" in self.html, "must block analysis without a backend")
        self.assertTrue("Conecta tu base de datos" in self.html, "missing honest unconnected state")


if __name__ == "__main__":
    unittest.main()
