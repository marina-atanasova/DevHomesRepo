from decimal import Decimal, ROUND_HALF_UP


DEFAULT_LIFE_INSURANCE_YEARLY_RATE = Decimal("0.0043")   # 0.43%
DEFAULT_PROPERTY_INSURANCE_YEARLY_RATE = Decimal("0.0027")  # 0.27%
DEFAULT_BANK_FEE_YEARLY_RATE = Decimal("0.0008")  # 0.08%

TWELVE = Decimal("12")
ONE_HUNDRED = Decimal("100")
MONEY_Q = Decimal("0.01")
BALANCE_TOLERANCE = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_Q, rounding=ROUND_HALF_UP)


def _to_decimal(value) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def simulate_repayment_plan(
    principal,
    yearly_interest_rate,
    monthly_payment,
    life_insurance_monthly=None,
    property_insurance_yearly=None,
    bank_fee_rate_yearly=None,
    max_months=1200,
):
    principal = _to_decimal(principal)
    yearly_interest_rate = _to_decimal(yearly_interest_rate)
    monthly_payment = _to_decimal(monthly_payment)

    if life_insurance_monthly in (None, ""):
        life_insurance_monthly = principal * DEFAULT_LIFE_INSURANCE_YEARLY_RATE / TWELVE
        used_default_life = True
    else:
        life_insurance_monthly = _to_decimal(life_insurance_monthly)
        used_default_life = False

    if property_insurance_yearly in (None, ""):
        property_insurance_yearly = principal * DEFAULT_PROPERTY_INSURANCE_YEARLY_RATE
        used_default_property = True
    else:
        property_insurance_yearly = _to_decimal(property_insurance_yearly)
        used_default_property = False

    if bank_fee_rate_yearly in (None, ""):
        bank_fee_rate_yearly = DEFAULT_BANK_FEE_YEARLY_RATE
        used_default_bank_fee = True
    else:
        bank_fee_rate_yearly = _to_decimal(bank_fee_rate_yearly) / ONE_HUNDRED
        used_default_bank_fee = False

    monthly_rate = (yearly_interest_rate / ONE_HUNDRED) / TWELVE
    property_insurance_monthly = property_insurance_yearly / TWELVE

    balance = principal
    months = 0

    total_bank_paid = Decimal("0")
    total_interest = Decimal("0")
    total_life_insurance = Decimal("0")
    total_property_insurance = Decimal("0")
    total_bank_fees = Decimal("0")

    while balance > BALANCE_TOLERANCE:
        if months >= max_months:
            raise ValueError("The repayment plan exceeds the maximum supported duration.")

        monthly_interest = balance * monthly_rate

        if monthly_payment <= monthly_interest:
            raise ValueError("Monthly payment is too low to repay this loan.")

        required_bank_payment = balance + monthly_interest
        actual_bank_payment = min(monthly_payment, required_bank_payment)
        principal_paid = actual_bank_payment - monthly_interest

        bank_fee_monthly = balance * bank_fee_rate_yearly / TWELVE

        total_bank_paid += actual_bank_payment
        total_interest += monthly_interest
        total_life_insurance += life_insurance_monthly
        total_property_insurance += property_insurance_monthly
        total_bank_fees += bank_fee_monthly

        balance -= principal_paid
        months += 1

    extra_costs_total = (
        total_interest
        + total_life_insurance
        + total_property_insurance
        + total_bank_fees
    )
    total_paid = total_bank_paid + total_life_insurance + total_property_insurance + total_bank_fees

    years = months // 12
    remaining_months = months % 12

    return {
        "months": months,
        "years": years,
        "remaining_months": remaining_months,
        "total_bank_paid": money(total_bank_paid),
        "total_interest": money(total_interest),
        "total_life_insurance": money(total_life_insurance),
        "total_property_insurance": money(total_property_insurance),
        "total_bank_fees": money(total_bank_fees),
        "extra_costs_total": money(extra_costs_total),
        "total_paid": money(total_paid),
        "life_insurance_monthly_used": money(life_insurance_monthly),
        "property_insurance_yearly_used": money(property_insurance_yearly),
        "bank_fee_rate_yearly_used_percent": money(bank_fee_rate_yearly * ONE_HUNDRED),
        "used_default_life": used_default_life,
        "used_default_property": used_default_property,
        "used_default_bank_fee": used_default_bank_fee,
    }


def calculate_early_repayment_comparison(
    principal,
    yearly_interest_rate,
    monthly_payment,
    early_monthly_payment,
    life_insurance_monthly=None,
    property_insurance_yearly=None,
    bank_fee_rate_yearly=None,
):
    original = simulate_repayment_plan(
        principal=principal,
        yearly_interest_rate=yearly_interest_rate,
        monthly_payment=monthly_payment,
        life_insurance_monthly=life_insurance_monthly,
        property_insurance_yearly=property_insurance_yearly,
        bank_fee_rate_yearly=bank_fee_rate_yearly,
    )

    early = simulate_repayment_plan(
        principal=principal,
        yearly_interest_rate=yearly_interest_rate,
        monthly_payment=early_monthly_payment,
        life_insurance_monthly=life_insurance_monthly,
        property_insurance_yearly=property_insurance_yearly,
        bank_fee_rate_yearly=bank_fee_rate_yearly,
    )

    savings = {
        "total_paid_saved": money(original["total_paid"] - early["total_paid"]),
        "extra_costs_saved": money(original["extra_costs_total"] - early["extra_costs_total"]),
        "interest_saved": money(original["total_interest"] - early["total_interest"]),
        "life_insurance_saved": money(original["total_life_insurance"] - early["total_life_insurance"]),
        "property_insurance_saved": money(original["total_property_insurance"] - early["total_property_insurance"]),
        "bank_fees_saved": money(original["total_bank_fees"] - early["total_bank_fees"]),
    }

    return {
        "original": original,
        "early": early,
        "savings": savings,
    }