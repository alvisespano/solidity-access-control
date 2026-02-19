import re
import pandas as pd
import sys
import argparse
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

### Regex for msg.sender checks

REQUIRE_SENDER_REGEX = re.compile(r'\brequire\s*\(\s*(?:msg\.sender\s*==|[^=]+==\s*msg\.sender)', re.MULTILINE)
ASSERT_SENDER_REGEX = re.compile(r'\bassert\s*\(\s*(?:msg\.sender\s*==|[^=]+==\s*msg\.sender)', re.MULTILINE)
IF_SENDER_REGEX = re.compile(r'\bif\s*\(\s*(?:msg\.sender\s*==|[^=]+==\s*msg\.sender)', re.MULTILINE)

def sender_checks(code: str) -> dict:
    return {
        "requiresender": len(REQUIRE_SENDER_REGEX.findall(code)) > 0,
        "assertsender": len(ASSERT_SENDER_REGEX.findall(code)) > 0,
        "ifsender": len(IF_SENDER_REGEX.findall(code)) > 0,
    }


def applyRegexSenderChecks(path, raw_code, code):
  
    senderChecks = sender_checks(code)

    return {
        "file": path,
        "require": senderChecks["requiresender"],
        "assert": senderChecks["assertsender"],
        "if": senderChecks["ifsender"],
    }


### Regex for Access Control OpenZeppelin Contracts

AC_DEFAULT_ADMIN_RULES_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bAccessControlDefaultAdminRules\b',
    re.IGNORECASE
)

AC_ENUMERABLE_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bAccessControlEnumerable\b',
    re.IGNORECASE
)

IAC_DEFAULT_ADMIN_RULES_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bIAccessControlDefaultAdminRules\b',
    re.IGNORECASE
)

IAC_ENUMERABLE_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bIAccessControlEnumerable\b',
    re.IGNORECASE
)

ACCESS_MANAGED_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bAccessManaged\b',
    re.IGNORECASE
)

ACCESS_MANAGER_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bAccessManager\b',
    re.IGNORECASE
)

AUTHORITY_UTILS_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bAuthorityUtils\b',
    re.IGNORECASE
)

IACCESS_MANAGED_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bIAccessManaged\b',
    re.IGNORECASE
)

IACCESS_MANAGER_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bIAccessManager\b',
    re.IGNORECASE
)

IAUTHORITY_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bIAuthority\b',
    re.IGNORECASE
)

ACCESS_CONTROL_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bAccessControl\b',
    re.IGNORECASE
)

IACCESS_CONTROL_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bIAccessControl\b',
    re.IGNORECASE
)

OWNABLE_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bOwnable\b',
    re.IGNORECASE
)

OWNABLE_2STEP_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bOwnable2Step\b',
    re.IGNORECASE
)

ACCESS_CONTROL_CROSSCHAIN_REGEX = re.compile(
    r'contract\s+\w+\s+is\s+[^{};]*\bAccessControlCrossChain\b',
    re.IGNORECASE
)

#AC_OPZ_CONTRACTS_REGEX = re.compile(r'contract\s+\w+\s+is\s+.*\b(AccessControlDefaultAdminRules | AccessControlEnumerable | IAccessControlDefaultAdminRules | IAccessControlEnumerable | AccessManaged | AccessManager | AuthorityUtils | IAccessManaged | IAccessManager | IAuthority | AccessControl | IAccessControl | Ownable | Ownable2Step | AccessControlCrossChain)\b', re.IGNORECASE)

OZ_ACCESS_IMPORT_REGEX = re.compile(
    r'import\s+["\']openzeppelin/contracts/access/[^"\']+["\']',
    re.MULTILINE
)

def findACContractOPZ(code: str) -> dict:
    return {
        "AccessControlDefaultAdminRules": len(AC_DEFAULT_ADMIN_RULES_REGEX.findall(code)) > 0,
        "AccessControlEnumerable": len(AC_ENUMERABLE_REGEX.findall(code)) > 0,
        "IAccessControlDefaultAdminRules": len(IAC_DEFAULT_ADMIN_RULES_REGEX.findall(code)) > 0,
        "IAccessControlEnumerable": len(IAC_ENUMERABLE_REGEX.findall(code)) > 0,
        "AccessManaged": len(ACCESS_MANAGED_REGEX.findall(code)) > 0,
        "AccessManager": len(ACCESS_MANAGER_REGEX.findall(code)) > 0,
        "AuthorityUtils": len(AUTHORITY_UTILS_REGEX.findall(code)) > 0,
        "IAccessManaged": len(IACCESS_MANAGED_REGEX.findall(code)) > 0,
        "IAccessManager": len(IACCESS_MANAGER_REGEX.findall(code)) > 0,
        "IAuthority": len(IAUTHORITY_REGEX.findall(code)) > 0,
        "AccessControl": len(ACCESS_CONTROL_REGEX.findall(code)) > 0,
        "IAccessControl": len(OWNABLE_REGEX.findall(code)) > 0,
        "Ownable": len(OWNABLE_2STEP_REGEX.findall(code)) > 0,
        "Ownable2Step": len(ACCESS_CONTROL_CROSSCHAIN_REGEX.findall(code)) > 0,
        "AccessControlCrossChain": len(OZ_ACCESS_IMPORT_REGEX.findall(code)) > 0,
    }

def applyRegexACContractOPZ(path, code):

    ac_contracts_opz = findACContractOPZ(code)

    return {
        "file": path,
        "AccessControlDefaultAdminRules": ac_contracts_opz["AccessControlDefaultAdminRules"],
        "AccessControlEnumerable": ac_contracts_opz["AccessControlEnumerable"],
        "IAccessControlDefaultAdminRules": ac_contracts_opz["IAccessControlDefaultAdminRules"],
        "IAccessControlEnumerable": ac_contracts_opz["IAccessControlEnumerable"],
        "AccessManaged": ac_contracts_opz["AccessManaged"],
        "AccessManager": ac_contracts_opz["AccessManager"],
        "AuthorityUtils": ac_contracts_opz["AuthorityUtils"],
        "IAccessManaged": ac_contracts_opz["IAccessManaged"],
        "IAccessManager": ac_contracts_opz["IAccessManager"],
        "IAuthority": ac_contracts_opz["IAuthority"],
        "AccessControl": ac_contracts_opz["AccessControl"],
        "IAccessControl": ac_contracts_opz["IAccessControl"],
        "Ownable": ac_contracts_opz["Ownable"],
        "Ownable2Step": ac_contracts_opz["Ownable2Step"],
        "AccessControlCrossChain": ac_contracts_opz["AccessControlCrossChain"],
    }


def applyRegexs(path, raw_code, code, option):
    
    if option == 'SENDERCHECKS':
        return applyRegexSenderChecks(path, raw_code, code)
    elif option == 'OPZCONTRACTS':
        return applyRegexACContractOPZ(path, raw_code)

    
    print(f"\n[Error during regex selection]: {option} not found")
    return None

# Strip comments and strings
def strip_comments_and_strings(code: str) -> str:
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
    code = re.sub(r"'(?:\\.|[^'\\])*'", "''", code)
    return code
    
# Read Solidity file
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"\n[Error during file reading {path}]: {e}")
        return None

# Analyze Solidity file
def analyze(path, option):
    raw_code = read_file(path)
    if raw_code is None:
        return None
   
    code = strip_comments_and_strings(raw_code)

    return applyRegexs(path, raw_code, code, option)

# Analyze list of Solidity files
def analyze_files(file_list, option):
    with open(file_list, "r", encoding="utf-8") as f:
        files = [l.strip() for l in f if l.strip()]

    results = []
    total = len(files)

    for i, file in enumerate(files, 1):
        results.append(analyze(file, option))
        print(f"\rProcessing {i}/{total}: {file}", end="")
        sys.stdout.flush()

    print("\nProcessing completed.")

    # None clean up
    return results

def parallelize_analyze_files(file_list, option, workers=None):
    with open(file_list, "r", encoding="utf-8") as f:
        files = [l.strip() for l in f if l.strip()]

    total = len(files)
    results = []

    if workers is None:
        workers = os.cpu_count()

    print(f"Using {workers} workers")

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(analyze, file, option): file
            for file in files
        }

        for i, future in enumerate(as_completed(futures), 1):
            file = futures[future]
            try:
                results.append(future.result())
            except Exception as e:
                print(f"\nError processing {file}: {e}")
                results.append(None)

            print(f"\rProcessing {i}/{total}", end="")
            sys.stdout.flush()

    print("\nProcessing completed.")
    return results

def get_count(counts, a, b, c):
            return counts.get((a, b, c), 0)
    
def print_figure_and_stats (results, option):
    df = pd.DataFrame(results)

    A = ""
    B = ""
    C = ""
    aVal = 0 
    bVal = 0
    abVal = 0 
    cVal = 0 
    acVal = 0 
    bcVal = 0 
    abcVal = 0

    outside = ""
    outsideVal = 0

    if option == 'SENDERCHECKS':

        A = "Require"
        B = "Assert"
        C = "If"
        outside = "No sender checks"

        combination_counts = df.groupby(["require", "assert", "if"]).size().reset_index(name="count")
        def comb_str(row):
            items = []
            for k in ["require", "assert", "if"]:
                if row[k]:
                    items.append(k)
            return " + ".join(items) if items else "none"
        combination_counts["combination"] = combination_counts.apply(comb_str, axis=1)
        combination_counts = combination_counts[["combination", "count"]].sort_values(by="count", ascending=False)
        
        counts = df.groupby(["require", "assert", "if"]).size()        

        aVal  = get_count(counts, True,  False, False)
        bVal  = get_count(counts, False, True,  False)
        cVal  = get_count(counts, False, False, True)

        abVal = get_count(counts, True,  True,  False)
        acVal = get_count(counts, True,  False, True)
        bcVal = get_count(counts, False, True,  True)
        abcVal = get_count(counts, True,  True,  True)

        no_sender_checks = df[~(df["require"] | df["assert"] | df["if"])]

        outsideVal  = len(no_sender_checks)

        print("\n=== Files WITHOUT sender checks ===")
        print(f"Total: {len(no_sender_checks)}")

        labels = (A, B, C)
        values = (aVal, bVal, abVal, cVal, acVal, bcVal, abcVal)

        print("\n=== INTERSECTION TABLE ===")

        print(f"{A} = {aVal}")
        print(f"{B} = {bVal}")
        print(f"{C} = {cVal}")
        print(f"{A} + {B} = {abVal}")
        print(f"{A} + {C} = {acVal}")
        print(f"{B} + {C} = {bcVal}")
        print(f"{A} + {B} + {C} = {abcVal}")
        print(f"{outside} = {outsideVal}")

        plt.figure(figsize=(6,6))
        v = venn3(subsets=values, set_labels=labels)

        plt.title("")

        plt.text(0, -1.2, f"{outside}: {outsideVal}", ha='center', fontsize=12)

        plt.savefig("/app/artifact/results/"+option+".pdf", format="pdf")
        plt.close()

        print(f"Generated figure: /app/artifact/results/{option}.pdf")
        
    elif option == 'OPZCONTRACTS':

        df["has_AccessControlDefaultAdminRules"] = df["AccessControlDefaultAdminRules"] > 0
        df["has_AccessControlEnumerable"] = df["AccessControlEnumerable"] > 0
        df["has_IAccessControlDefaultAdminRules"] = df["IAccessControlDefaultAdminRules"] > 0
        df["has_IAccessControlEnumerable"] = df["IAccessControlEnumerable"] > 0
        df["has_AccessManaged"] = df["AccessManaged"] > 0
        df["has_AccessManager"] = df["AccessManager"] > 0
        df["has_AuthorityUtils"] = df["AuthorityUtils"] > 0
        df["has_IAccessManaged"] = df["IAccessManaged"] > 0
        df["has_IAccessManager"] = df["IAccessManager"] > 0
        df["has_IAuthority"] = df["IAuthority"] > 0
        df["has_AccessControl"] = df["AccessControl"] > 0
        df["has_IAccessControl"] = df["IAccessControl"] > 0
        df["has_Ownable"] = df["Ownable"] > 0
        df["has_Ownable2Step"] = df["Ownable2Step"] > 0
        df["has_AccessControlCrossChain"] = df["AccessControlCrossChain"] > 0

        #counts = df.groupby(["has_AccessControlDefaultAdminRules", "has_AccessControlEnumerable", "has_IAccessControlDefaultAdminRules", "has_IAccessControlEnumerable", "has_AccessManaged", "has_AccessManager", "has_AuthorityUtils", "has_IAccessManaged", "has_IAccessManager", "has_IAuthority", "has_AccessControl", "has_IAccessControl", "has_Ownable", "has_Ownable2Step", "has_AccessControlCrossChain"]).size()
        noAC = (~(df["has_AccessControlDefaultAdminRules"] | df["has_AccessControlEnumerable"] | df["has_IAccessControlDefaultAdminRules"] | df["has_IAccessControlEnumerable"] | df["has_AccessManaged"] | df["has_AccessManager"] | df["has_AuthorityUtils"] | df["has_IAccessManaged"] | df["has_IAccessManager"] | df["has_IAuthority"] | df["has_AccessControl"] | df["has_IAccessControl"] | df["has_Ownable"] | df["has_Ownable2Step"] | df["has_AccessControlCrossChain"])).sum()

        yesAC = ((df["has_AccessControlDefaultAdminRules"] | df["has_AccessControlEnumerable"] | df["has_IAccessControlDefaultAdminRules"] | df["has_IAccessControlEnumerable"] | df["has_AccessManaged"] | df["has_AccessManager"] | df["has_AuthorityUtils"] | df["has_IAccessManaged"] | df["has_IAccessManager"] | df["has_IAuthority"] | df["has_AccessControl"] | df["has_IAccessControl"] | df["has_Ownable"] | df["has_Ownable2Step"] | df["has_AccessControlCrossChain"])).sum()

        print(f"Contract with Access Control Patterns of OpenZeppelin: {yesAC}")    
        print(f"Other Contracts: {noAC}")       
  

# *** Main method ***

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("file_list", help="TXT file containing Solidity file paths to analyze")
    parser.add_argument("option", help="regexs to run (SENDERCHECKS, OPZCONTRACTS)")
    args = parser.parse_args()
    
    results = parallelize_analyze_files(args.file_list, args.option)

    # None clean up
    results = [x for x in results if x is not None]
    
    print_figure_and_stats(results, args.option)