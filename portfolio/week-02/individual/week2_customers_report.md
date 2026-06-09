# Week 2 Individual Cleaning Report: Customer Data

**Role:** Customer Data Cleaner
**Object:** Table `customers` (Supabase)
**Objective:** Identify data quality issues (duplicates, NULL values, formatting errors) and present proposals for data remediation.

## 1. Methodology and Security
In accordance with the requirements of UrbanStyle's IT Director, the analysis was conducted on a **test copy** to avoid putting the live source data at risk.
* Table created: `customers_test`.
* Original row count: `3150` rows.

## 2. Data Quality Summary Report

| Category | Issues Found | Description |
| :--- | :--- | :--- |
| **Duplicate emails** | `128` | The same email is associated with multiple different customer records. |
| **NULL first name** | `0` | Customer's first name is missing or the field is empty. |
| **NULL last name** | `0` | Customer's last name is missing or the field is empty. |
| **Inconsistent city names** | `54` | Varying name formats (e.g., "tallinn" vs "Tallinn"). |
| **NULL phone/email** | `0 (phone) / 380 (email)` | Missing contact details for marketing purposes. |
| **TOTAL issues** | **`562`** | |

## 3. Detailed Analysis

### 3.1. Duplicates and Contact Information
It was identified that `128` email addresses are repeated in the database. This indicates that some customers are recorded multiple times in the system, which distorts the actual size of the customer base.

### 3.2. Formatting Errors and Missing Names
Checking the city names revealed that `54` different variations are in use (e.g., leading spaces or inconsistent capitalization). The audit also confirmed that all customers have their first and last names filled out (number of missing names: 0).

## 4. Implement Improvements (Advanced Level)

Following the IT Director's instructions, data transformation was carried out in the test table `customers_test`. The table below compares the state of the data before and after the cleaning process was applied.

| Category | Before Cleaning | After Cleaning | Activity Description |
| :--- | :--- | :--- | :--- |
| **City names** | 54 unique variations | 12 unique variations | Capitalization standardized and whitespaces removed using the `INITCAP` and `TRIM` functions. |
| **Customer names** | 0 missing records | 0 missing records | Verified that first and last names are fully populated. No NULL values or empty strings were detected. |
| **Emails** | 0 non-standard records | 0 non-standard records | Converting addresses to lowercase (`LOWER`) and removing spaces (`TRIM`) resulted in no changes. |
| **Phone numbers** | All 3150 records standard | All 3150 records standard | Identified via `CASE WHEN` logic and a subquery that all existing phone numbers already conform to the standard. |

### Cleaning Impact and Conclusions
1. **Data Consistency:** Standardizing city names (e.g., "tallinn" -> "Tallinn") ensures that future sales analysis by location is 100% accurate and does not scatter data across different spelling variations.
2. **Quality Assurance:** The fact that there are no nameless customers in the database (0 findings) demonstrates that the customer registration process is functional in this regard, though it requires ongoing monitoring.
3. **Marketing Readiness:** The contact data audit confirmed that emails and phone numbers are in the correct format and required no additional standardization (0 corrections). This gives the marketing team confidence that campaigns will reach recipients without technical glitches and confirms the reliability of existing data entry practices.

## 5. Recommendation to the IT Director
The most critical issue is the **missing emails**, as this constitutes a **direct obstacle to marketing activities** in the database, preventing UrbanStyle from communicating with its customers and sending them promotional offers. Customers without contact information represent a "blind spot" for the company, making it impossible to calculate an accurate **marketing ROI** or compile the data-driven business plan required by investors, since the true size and loyalty of the customer base remain unclear. I recommend implementing a **mandatory email field validation** during data entry, which would prevent the creation of a new customer record without valid contact information, thereby avoiding the accumulation of anonymous and useless data in the future.