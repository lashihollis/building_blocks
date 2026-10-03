from abc import ABC, abstractmethod


class DataQualityCheck(ABC):

    def __init__(self, table_name, column, data, sample_limit=5,):
        self._table_name = table_name
        self._column = column
        self._data = data
        self._sample_limit = sample_limit

    def add_failed_id(self, failed_ids, claim_id):
        if len(failed_ids) < self._sample_limit:
            failed_ids.append(claim_id)

    @abstractmethod
    def run(self):
        pass

class NullCheck(DataQualityCheck):

    def run(self):
        null_count = 0
        failed_ids = []

        for row in self._data:
            value = row[self._column]

            if value is None:
                null_count += 1
                self.add_failed_id(failed_ids, row["claim_id"])

        return {
            "check": self.__class__.__name__,
            "table_name": self._table_name,
            "column": self._column,
            "failure_count": null_count,
            "failed_ids": failed_ids,
            "passed": null_count == 0
        }

class DuplicateCheck(DataQualityCheck):

    def run(self):
        seen = set()
        dupe_count = 0
        failed_ids = []

        for row in self._data:
            value = row[self._column]

            if value in seen:
                dupe_count += 1
                self.add_failed_id(failed_ids, row["claim_id"])
            else:
                seen.add(value)

        return {
            "check": self.__class__.__name__,
            "table_name": self._table_name,
            "column": self._column,
            "failure_count": dupe_count,
            "failed_ids": failed_ids,
            "passed": dupe_count == 0
        }

class NegativeValueCheck(DataQualityCheck):

    def run(self):
        negative_count = 0
        failed_ids = []

        for row in self._data:
            value = row[self._column]

            if value is None:
                continue

            if value < 0:
                negative_count += 1
                self.add_failed_id(failed_ids, row["claim_id"])

        return {
            "check": self.__class__.__name__,
            "table_name": self._table_name,
            "column": self._column,
            "failure_count": negative_count,
            "failed_ids": failed_ids,
            "passed": negative_count == 0
        }

class RangeCheck(DataQualityCheck):

    def __init__(self, table_name, column, data, minimum, maximum):
        super().__init__(table_name, column, data)
        self._minimum = minimum
        self._maximum = maximum

    def run(self):
        outside_range_count = 0
        failed_ids = []

        for row in self._data:
            value = row[self._column]

            if value is None:
                continue

            if value < self._minimum or value > self._maximum:
                outside_range_count += 1
                self.add_failed_id(failed_ids, row["claim_id"])

        return {
            "check": self.__class__.__name__,
            "table_name": self._table_name,
            "column": self._column,
            "failure_count": outside_range_count,
            "failed_ids": failed_ids,
            "passed": outside_range_count == 0
        }

class DeniedClaimAmountCheck(DataQualityCheck):

    def run(self):
        failure_count = 0
        failed_ids = []

        for row in self._data:
            status = row["status"]
            amount = row["claim_amount"]

            if amount is None:
                continue

            if status == "denied" and amount > 0:
                failure_count += 1
                self.add_failed_id(failed_ids, row["claim_id"])

        return {
            "check": self.__class__.__name__,
            "table_name": self._table_name,
            "column": "status + claim_amount",
            "failure_count": failure_count,
            "failed_ids": failed_ids,
            "passed": failure_count == 0
        }

class ValidValuesCheck(DataQualityCheck):

    def __init__(self, table_name, column, data, valid_values):
        super().__init__(table_name, column, data)
        self._valid_values = valid_values

    def run(self):
        invalid_count = 0
        failed_ids = []

        for row in self._data:
            value = row[self._column]

            if value is None:
                continue

            if value not in self._valid_values:
                invalid_count += 1
                self.add_failed_id(failed_ids, row["claim_id"])

        return {
            "check": self.__class__.__name__,
            "table_name": self._table_name,
            "column": self._column,
            "failure_count": invalid_count,
            "failed_ids": failed_ids,
            "passed": invalid_count == 0
        }

class DataQualitySuite:

    def __init__(self):
        self.checks = []

    def add_check(self, check):
        self.checks.append(check)

    def run_all(self):
        results = []

        for check in self.checks:
            result = check.run()
            results.append(result)

        return results

claims = []

for i in range(1, 10001):

    claim = {
        "claim_id": i,
        "patient_id": 1000 + i,
        "claim_amount": 100,
        "status": "paid"
    }

    if 2400 < i <= 4100:
        claim["claim_amount"] = 10000

    if 2200 < i <= 2400:
        claim["status"] = "denied"

    if 1700 < i <= 2200:
        claim["status"] = "INVALID"

    if 700 < i <= 1700:
        claim["claim_amount"] = -100

    if i <= 700:
        claim["claim_amount"] = None

    claims.append(claim)


# Create the suite
suite = DataQualitySuite()

# Create the checks
null_check = NullCheck(
    table_name="claims",
    column="claim_amount",
    data=claims
)

duplicate_check = DuplicateCheck(
    table_name="claims",
    column="claim_id",
    data=claims
)

negative_check = NegativeValueCheck(
    table_name="claims",
    column="claim_amount",
    data=claims
)

range_check = RangeCheck(
    table_name="claims",
    column="claim_amount",
    data=claims,
    minimum=0,
    maximum=5000
)

denied_check = DeniedClaimAmountCheck(
    table_name="claims",
    column="claim_amount",
    data=claims
)

validity_check = ValidValuesCheck(
    table_name="claims",
    column="status",
    data=claims,
    valid_values=["paid", "denied", "pending"]
)

# Add checks to the suite
suite.add_check(null_check)
suite.add_check(duplicate_check)
suite.add_check(negative_check)
suite.add_check(range_check)
suite.add_check(denied_check)
suite.add_check(validity_check)

# Run all checks
results = suite.run_all()

# Print each result
for result in results:
    print(result)