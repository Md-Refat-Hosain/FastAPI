from pydantic import BaseModel


class CstmrChrn(BaseModel):
    seniorcitizen: int
    tenure: float
    monthlycharges: float
    gender_male: int
    partner_yes: int
    dependents_yes: int
    phoneservice_yes: int
    multiplelines_yes: int
    internetservice_fiber_optic: int
    internetservice_no: int
    onlinesecurity_yes: int
    onlinebackup_yes: int
    deviceprotection_yes: int
    techsupport_yes: int
    streamingtv_yes: int
    streamingmovies_yes: int
    contract_one_year: int
    contract_two_year: int
    paperlessbilling_yes: int
    paymentmethod_credit_card: int
    paymentmethod_electronic_check: int
    paymentmethod_mailed_check: int
