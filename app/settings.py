from sdx_base.settings.app import AppSettings, get_settings


class Settings(AppSettings):
    receipt_subscription_id: str = "dap-receipt-subscription"
    expiry_days: int = 90

    def get_output_bucket_name(self) -> str:
        return f"{self.project_id}-outputs"

    def get_seft_bucket_name(self) -> str:
        return f"{self.project_id}-seft-responses"

    def get_survey_bucket_name(self) -> str:
        return f"{self.project_id}-survey-responses"


def get_instance() -> Settings:
    return get_settings(Settings)
