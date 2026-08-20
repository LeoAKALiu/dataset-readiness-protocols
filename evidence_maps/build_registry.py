#!/usr/bin/env python3
"""Build the family-level registry used by the 2026-08-19 four-source merge.

Input is the JSONL appendix embedded in local DeepResearch report S2.  The
other three reports did not provide a complete machine-readable registry, so
their candidate names and the cross-check corrections are declared below.
This script assigns no DRRL or ERL score.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


FIELDS = [
    "family_key",
    "canonical_name",
    "aliases",
    "cluster",
    "eligibility_status",
    "scope_fit",
    "task_types",
    "modality",
    "release_span",
    "public_asset_state",
    "license",
    "persistent_id",
    "primary_url",
    "evidence_grade",
    "source_count",
    "source_flags",
    "verification_note",
]


def slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("/", " ").replace("–", " ").replace("—", " ")
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text


KEY_ALIASES = {
    "sdnet2018": "sdnet2018",
    "codebrim": "codebrim",
    "segcodebrim": "codebrim",
    "dacl10k": "dacl",
    "dacl1k": "dacl",
    "road_damage_dataset": "rdd",
    "rdd2018": "rdd",
    "rdd2022": "rdd",
    "concrete_crack_images_for_classification": "metu_concrete_crack",
    "metu": "metu_concrete_crack",
    "cracktree200_cracktree260": "cracktree",
    "cracktree200": "cracktree",
    "cracktree260": "cracktree",
    "gaps_gaps384": "gaps",
    "gaps384": "gaps",
    "gtsrb_gtsdb": "gtsrb_gtsdb",
    "whu_building_dataset": "whu_building",
    "whu_building_dataset_aerial": "whu_building",
    "gyu_det_bridge_defect_dataset": "gyu_det",
    "gyu_det": "gyu_det",
    "bridge_3d_segmentation_dataset": "semanticbridge",
    "bridge_3d_segmentation_dataset_2025": "semanticbridge",
    "bridge_3d_semantic_segmentation_dataset": "semanticbridge",
    "tack_tunnel_data": "ttd",
    "ttd": "ttd",
    "crackforest_dataset": "cfd",
    "cfd": "cfd",
    "mfnet_dataset": "mfnet",
    "mfnet": "mfnet",
    "kaist_multispectral": "kaist_multispectral",
    "kaist_multispectral_pedestrian": "kaist_multispectral",
    "kaist_multispectral_pedestrian_dataset": "kaist_multispectral",
    "rohbau3d_semantics": "rohbau3d",
    "rohbau3d": "rohbau3d",
    "whu_urban3d": "whu_urban3d",
    "whu_railway3d": "whu_railway3d",
    "osv_street_view": "osv",
    "osv": "osv",
    "labeled_cracks_in_the_wild": "lcw",
    "lcw": "lcw",
    "bd3": "bd3",
    "whu_mix": "whu_mix",
    "semantickitti": "semantic_kitti",
}


def family_key(name: str) -> str:
    raw = slug(name)
    for prefix in ("dataset_",):
        if raw.startswith(prefix):
            raw = raw[len(prefix):]
    return KEY_ALIASES.get(raw, raw)


def cluster_of(value: str) -> str:
    value = value.strip()
    if value.startswith("A"):
        return "A"
    if value.startswith("B"):
        return "B"
    if value.startswith("C"):
        return "C"
    if value.startswith("D"):
        return "D"
    if value == "future_scope":
        return "future_scope"
    return "excluded"


def text_list(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def base_record(obj: dict) -> dict:
    name = obj["official_name"]
    key = family_key(name)
    status = obj["eligibility_status"]
    disputed = "disputed" in obj.get("cluster_candidate", "") or "provisional" == status
    scope_fit = {
        "future_scope": "future_scope",
        "exclude": "out_of_scope_or_nonpublic",
        "inventory_only": "in_scope_no_public_asset",
    }.get(status, "boundary_review" if disputed else "in_scope")
    access = obj.get("access_status", "")
    asset_state = "claimed_or_reported"
    if status == "inventory_only":
        asset_state = "not_located"
    elif status == "exclude":
        asset_state = "not_eligible"
    elif "active" in access.lower() or "verified" in access.lower():
        asset_state = "reported_active"
    return {
        "family_key": key,
        "canonical_name": name,
        "aliases": text_list(obj.get("aliases")),
        "cluster": cluster_of(obj.get("cluster_candidate", "")),
        "eligibility_status": status,
        "scope_fit": scope_fit,
        "task_types": text_list(obj.get("task_types")),
        "modality": obj.get("modality", ""),
        "release_span": str(obj.get("release_year", "")),
        "public_asset_state": asset_state,
        "license": obj.get("license", ""),
        "persistent_id": obj.get("doi") or "",
        "primary_url": obj.get("official_dataset_url") or "",
        "evidence_grade": obj.get("evidence_confidence", ""),
        "source_count": "1",
        "source_flags": "S2_local",
        "verification_note": obj.get("eligibility_reason", ""),
    }


def rec(
    key: str,
    name: str,
    cluster: str,
    status: str,
    tasks: str,
    modality: str,
    source: str,
    *,
    aliases: str = "",
    release: str = "",
    scope: str = "in_scope",
    asset: str = "source_report_only",
    license_: str = "",
    pid: str = "",
    url: str = "",
    grade: str = "Q1",
    note: str = "",
) -> dict:
    return {
        "family_key": key,
        "canonical_name": name,
        "aliases": aliases,
        "cluster": cluster,
        "eligibility_status": status,
        "scope_fit": scope,
        "task_types": tasks,
        "modality": modality,
        "release_span": release,
        "public_asset_state": asset,
        "license": license_,
        "persistent_id": pid,
        "primary_url": url,
        "evidence_grade": grade,
        "source_count": "1",
        "source_flags": source,
        "verification_note": note,
    }


ADDITIONS = [
    # S1 local report additions not present in the S2 registry.
    rec("infracracknet", "InfraCrackNet dataset", "A", "provisional", "segmentation", "2D RGB", "S1_local", release="2025", scope="boundary_review", note="Paper claims data release; official distribution asset not rechecked."),
    rec("concrete_beam_column_2025", "Concrete beam/column crack dataset (2025)", "A", "provisional", "classification; detection", "2D RGB", "S1_local", release="2025", scope="boundary_review", note="Data-paper identity reported; repository and exact dataset title still require normalization."),
    rec("bridge_culvert_crack_6900", "Bridge/culvert crack benchmark (6900+ images)", "A", "inventory_only", "classification", "2D RGB", "S1_local", release="2021", scope="in_scope_no_public_asset", asset="not_located", note="Conference paper claims a benchmark; stable distribution asset not located."),
    rec("bikit", "bikit Building Inspection Toolkit", "excluded", "exclude", "aggregation/toolkit", "software/aggregator", "S1_local", release="2022", scope="not_a_dataset", asset="not_eligible", url="https://github.com/iarai/bikit", grade="Q2", note="Data aggregation toolkit, not an independently acquired dataset family."),
    rec("rome_road_damage", "Rome Road Damage Dataset", "A", "include", "object detection", "2D RGB", "S1_local", release="2026", asset="primary_record_verified", pid="10.1038/s41598-026-46679-4", url="https://doi.org/10.1038/s41598-026-46679-4", grade="Q2", note="Road cracks, potholes and manholes; distinct from the RDD competition family."),
    rec("winleak", "WinLeak", "B", "include", "segmentation; leakage localization", "paired RGB-thermal", "S1_local;S3_grok", release="2025", asset="paper_and_release_claim_verified", pid="10.1145/3736425.3770112", url="https://doi.org/10.1145/3736425.3770112", grade="Q2", note="Building-window air-leakage data; verify exact file-level license during DRRL."),
    rec("thermoscenes", "ThermoScenes", "future_scope", "future_scope", "thermal reconstruction; temperature estimation", "RGB-thermal", "S1_local", release="2024", scope="task_outside_current_protocol", asset="source_report_only", note="No classification/detection/segmentation target under the current Cluster B boundary."),
    rec("zaha", "ZAHA façade point-cloud dataset", "C", "include", "semantic segmentation", "3D façade point cloud", "S1_local", release="2025", asset="paper_identity_verified", pid="10.1109/WACV61041.2025.00743", url="https://doi.org/10.1109/WACV61041.2025.00743", grade="Q2", note="Distribution package still requires file-level DRRL verification."),
    rec("cus3d", "CUS3D", "C", "provisional", "semantic segmentation", "point cloud; mesh; 2D imagery", "S1_local", release="2024", scope="boundary_review", note="Public benchmark claimed; official distribution asset not rechecked."),
    rec("opentrench3d", "OpenTrench3D", "C", "include", "semantic segmentation", "photogrammetric point cloud", "S1_local", release="2024", asset="reported_active", grade="Q2", note="Underground-utility trench scenes fit infrastructure point-cloud scope."),
    rec("archx_3m", "3M / ArCHX", "C", "provisional", "semantic segmentation", "UAV photogrammetric point cloud", "S1_local", release="2025", scope="boundary_review", note="Family name and distribution relationship require primary-source resolution."),
    rec("hrhd_hk", "HRHD-HK", "C", "provisional", "semantic segmentation", "photogrammetric point cloud", "S1_local", release="2023", scope="boundary_review", note="Benchmark is described in a paper; distribution asset not rechecked."),
    rec("urban_footpath", "Urban Footpath Image Dataset", "D", "provisional", "detection; segmentation", "2D street-level RGB", "S1_local", aliases="Crowd4Access", release="2021", scope="boundary_review", note="Urban furniture/footpath fit is strong, but distribution entry remains unresolved."),

    # S3 Grok report additions.
    rec("cif", "Cracks in Foundation (CiF)", "A", "provisional", "classification; detection; segmentation", "2D RGB", "S3_grok", release="2026", scope="boundary_review", pid="arXiv:2605.18413", url="https://arxiv.org/abs/2605.18413", grade="Q2", note="Preprint identity verified; public asset and license require independent check."),
    rec("nccd_pf", "NCCD-PF", "A", "include", "crack classification", "2D RGB", "S3_grok", release="2023", asset="paper_identity_verified", pid="10.1038/s41597-023-02839-z", url="https://doi.org/10.1038/s41597-023-02839-z", grade="Q2", note="Nature Scientific Data descriptor; file-level access verification remains for DRRL."),
    rec("pavedistress", "PaveDistress", "A", "include", "pavement distress classification; detection", "2D RGB", "S3_grok", asset="primary_record_verified", pid="10.17632/f46zt2g83x.1", url="https://data.mendeley.com/datasets/f46zt2g83x/1", grade="Q2", note="Mendeley Data identity verified."),
    rec("mdmcs", "MDMCS", "A", "include", "multi-defect detection/classification", "2D RGB", "S3_grok", release="2024", asset="primary_record_verified", pid="10.17632/6x4dzzrs2h.2", url="https://data.mendeley.com/datasets/6x4dzzrs2h/2", grade="Q2", note="Mendeley Data record and paper DOI 10.1061/JBENF2.BEENG-7893 verified."),
    rec("bcl", "Bridge Crack Library (BCL)", "A", "provisional", "crack classification; detection", "2D RGB", "S3_grok", scope="boundary_review", note="Dataset identity reported, but official asset and lineage remain unresolved."),
    rec("tbbr", "Thermal Bridges on Building Rooftops (TBBR)", "B", "include", "thermal-bridge detection; segmentation", "paired/registered RGB-thermal", "S3_grok", release="2023", asset="primary_record_verified", license_="CC BY 4.0", pid="10.5281/zenodo.7360996; 10.5281/zenodo.4767771", url="https://zenodo.org/records/7360996", grade="Q2", note="Raw and annotated releases are separate version nodes of one acquisition family."),
    rec("tufseg", "TUFSeg", "B", "include", "façade thermal segmentation", "paired RGB-thermal", "S3_grok", release="2024", asset="primary_record_verified", license_="CC BY 4.0", pid="10.5281/zenodo.10814413", url="https://zenodo.org/records/10814413", grade="Q2", note="Zenodo record verified; relationship to other thermal-façade acquisitions requires Q3 hash check."),
    rec("kust4k", "Kust4K", "B", "include", "RGB-thermal semantic segmentation", "paired RGB-thermal", "S3_grok", release="2025", asset="paper_identity_verified", pid="10.1038/s41597-025-05994-7", url="https://doi.org/10.1038/s41597-025-05994-7", grade="Q2", note="Scientific Data descriptor verified."),
    rec("tir_rgb_uav", "TIR-RGB-UAV Part 2", "B", "include", "detection; segmentation", "paired UAV thermal-RGB", "S3_grok", release="2026", asset="primary_record_verified", license_="CC BY-NC 4.0", pid="10.57760/sciencedb.28093", url="https://doi.org/10.57760/sciencedb.28093", grade="Q2", note="DataCite says 2026, correcting the report's 2025 date."),
    rec("asphalt_ir_visible", "Asphalt infrared-visible crack severity dataset", "B", "include", "crack severity classification", "paired infrared-visible", "S3_grok", release="2024", asset="primary_record_verified", license_="CC BY 4.0", pid="10.5281/zenodo.11625820", url="https://zenodo.org/records/11625820", grade="Q2", note="Zenodo identity and license verified."),
    rec("city_facade", "City-Facade", "C", "include", "façade semantic segmentation", "3D point cloud", "S3_grok", release="2026", asset="paper_identity_verified", pid="10.1016/j.isprsjprs.2026.01.003", url="https://doi.org/10.1016/j.isprsjprs.2026.01.003", grade="Q2", note="Paper identity verified; public data package still needs DRRL probe."),
    rec("semanticurban", "SemanticUrban", "C", "include", "urban point-cloud semantic segmentation", "3D point cloud", "S3_grok", release="2026", asset="paper_identity_verified", pid="10.1016/j.eswa.2026.132949", url="https://doi.org/10.1016/j.eswa.2026.132949", grade="Q2", note="Paper identity verified; data distribution needs file-level check."),
    rec("whu_infra3d", "WHU-Infra3D", "C", "provisional", "infrastructure point-cloud segmentation", "3D point cloud", "S3_grok", release="2026", scope="boundary_review", pid="arXiv:2606.09882", url="https://arxiv.org/abs/2606.09882", grade="Q2", note="Preprint identity verified; distribution and license not yet verified."),
    rec("pc_urban", "PC-Urban", "C", "include", "urban point-cloud segmentation", "3D point cloud", "S3_grok", asset="primary_record_verified", license_="CC BY 4.0", pid="10.21227/fvqd-k603", url="https://doi.org/10.21227/fvqd-k603", grade="Q2", note="IEEE DataPort/DataCite identity and license verified."),
    rec("uns_geo", "UNS Geo", "C", "provisional", "urban point-cloud segmentation", "3D point cloud", "S3_grok", scope="boundary_review", note="Official asset and canonical title unresolved."),
    rec("estate", "ESTATE", "C", "provisional", "urban point-cloud segmentation", "3D point cloud", "S3_grok", scope="boundary_review", note="Acronym collision and public distribution require primary-source resolution."),
    rec("urbanlf", "UrbanLF", "D", "provisional", "urban asset detection; segmentation", "2D street-level RGB", "S3_grok", scope="boundary_review", note="Official asset and exact canonical title unresolved."),
    rec("urban_electrical_distribution", "Urban Electrical Distribution Dataset", "D", "provisional", "electrical asset detection", "2D RGB", "S3_grok", scope="boundary_review", note="Public release and license require primary verification."),
    rec("sydney_urban_objects", "Sydney Urban Objects", "C", "include", "urban-object classification/detection", "3D point cloud", "S3_grok", release="2013", asset="reported_active", grade="Q2", note="Reclassified from Grok's D to C because the released observations are 3D point clouds."),
    rec("builtupunits", "BuiltUpUnits", "future_scope", "future_scope", "urban morphology/GIS", "geospatial vector/raster", "S3_grok", scope="outside_current_visual_clusters", note="Retained for later GIS extension; not scored under A-D."),
    rec("cmab", "CMAB", "future_scope", "future_scope", "urban assessment", "GIS/tabular", "S3_grok", scope="outside_current_visual_clusters", note="Acronym identity needs clarification before any future-scope use."),
    rec("ghs_ucdb", "GHS-UCDB", "future_scope", "future_scope", "urban centre database", "GIS/tabular", "S3_grok", scope="outside_current_visual_clusters", note="Urban context source, not a visual inspection dataset under A-D."),
    rec("actgov", "ACTGOV", "future_scope", "future_scope", "urban governance indicators", "tabular", "S3_grok", scope="outside_current_visual_clusters", note="Policy/context data, not a visual dataset under A-D."),

    # S4 Gemini report additions not present in the S2 registry.
    rec("bd3", "BD3 Building Defects Detection Dataset", "A", "provisional", "classification", "2D RGB", "S4_gemini", release="2024", scope="boundary_review", asset="samples_and_code_verified_full_asset_unclear", pid="10.1145/3671127.3698789", url="https://github.com/Praveenkottari/BD3-Dataset", grade="Q2", note="Repository contains code and samples, not the full 3,965-image asset; Kaggle mirror has unknown license."),
    rec("lcw", "Labeled Cracks in the Wild (LCW)", "A", "include", "semantic segmentation", "2D RGB", "S4_gemini", release="2021 v1-v2", asset="primary_record_verified", license_="CC0", pid="10.7294/16624672", url="https://data.lib.vt.edu/articles/dataset/Labeled_Cracks_in_the_Wild_LCW_Dataset/16624672", grade="Q2", note="3,817 annotated structural-inspection images; Gemini cited the code repo instead of the canonical dataset record."),
    rec("rohbau3d", "Rohbau3D", "C", "include", "semantic segmentation; instance segmentation", "TLS point cloud", "S4_gemini", aliases="Rohbau3D-Semantics", release="2025; semantics extension current", asset="primary_record_and_repo_verified", license_="MIT repository; dataset terms to verify", pid="10.1038/s41597-025-05827-7", url="https://github.com/RauchLukas/Rohbau3D", grade="Q2", note="504 scans across 14 sites; placeholder Zenodo DOI in Gemini is invalid."),
    rec("whu_urban3d", "WHU-Urban3D", "C", "include", "semantic segmentation; instance segmentation; 3D detection", "ALS and MLS point cloud", "S4_gemini", release="v1", asset="official_portal_verified_registration_required", url="https://whu3d.com/dataset/", grade="Q2", note="Official portal reports 3.6 million m2 and more than 300 million points."),
    rec("whu_railway3d", "WHU-Railway3D", "C", "include", "semantic segmentation", "railway MLS point cloud", "S4_gemini", release="2024", asset="official_repository_verified", pid="10.1109/TITS.2024.3469546", url="https://github.com/WHU-USI3DV/WHU-Railway3D", grade="Q2", note="30 km total and about 4.6 billion points; Gemini's DOI placeholder is invalid."),
    rec("osv", "Omnidirectional Street-View (OSV) Dataset", "D", "include", "spherical object detection", "panoramic RGB", "S4_gemini", release="2019", asset="official_portal_verified", url="https://gpcv.whu.edu.cn/data/osv_page.html", grade="Q2", note="Official page reports 5,636 objects; 1,777 refers to lights, not image count."),
    rec("whu_mix", "WHU-Mix building dataset", "D", "include", "building segmentation; polygon extraction", "aerial/satellite RGB", "S4_gemini", release="raster; vector derivative", asset="official_portal_verified", url="https://gpcv.whu.edu.cn/data/", grade="Q2", note="Gemini discusses this family but omits it from its own 15-row registry and count."),
    rec("whu_3dbie_solarpv", "WHU 3DBIE-SolarPV", "future_scope", "future_scope", "solar-potential estimation", "3D building/GIS", "S4_gemini", scope="outside_current_visual_tasks", url="https://github.com/WHU-USI3DV/3DBIE-SolarPV", grade="Q2", note="Related to urban renewal planning but not a current A-D perception task."),
    rec("bijie_landslide", "Bijie Landslide Dataset", "future_scope", "future_scope", "landslide mapping", "remote sensing", "S4_gemini", scope="outside_current_visual_tasks", note="Disaster remote sensing, outside the current urban-asset/inspection clusters."),
    rec("maduo_earthquake_crack", "Maduo Earthquake Crack Dataset", "future_scope", "future_scope", "earthquake crack detection", "aerial remote sensing", "S4_gemini", scope="outside_current_visual_tasks", url="https://gpcv.whu.edu.cn/data/", grade="Q2", note="Official WHU portal verifies the dataset; retained outside A-D for now."),
]


SOURCE_MENTIONS = {
    "S1_local": {
        "sdnet2018", "codebrim", "infracracknet", "concrete_beam_column_2025",
        "bridge_culvert_crack_6900", "bikit", "rdd", "rome_road_damage", "pst900",
        "winleak", "thermoscenes", "toronto_3d", "paris_lille_3d", "sensaturban",
        "zaha", "cus3d", "opentrench3d", "archx_3m", "hrhd_hk", "mapillary_vistas",
        "cityscapes", "urban_footpath",
    },
    "S3_grok": {
        "sdnet2018", "metu_concrete_crack", "codebrim", "cfd", "crack500", "deepcrack",
        "rdd", "dacl", "cif", "nccd_pf", "pavedistress", "mdmcs", "crackseg9k",
        "structdamage", "bcl", "tbbr", "tufseg", "kust4k", "tir_rgb_uav",
        "asphalt_ir_visible", "sensaturban", "toronto_3d", "city_facade", "semanticurban",
        "whu_infra3d", "pc_urban", "uns_geo", "estate", "cityscapes", "mapillary_vistas",
        "tt100k", "urbanlf", "urban_electrical_distribution", "sydney_urban_objects",
        "builtupunits", "cmab", "ghs_ucdb", "actgov", "winleak",
    },
    "S4_gemini": {
        "sdnet2018", "dacl", "codebrim", "bd3", "gyu_det", "lcw", "ttd", "s2ds",
        "mfnet", "kaist_multispectral", "rohbau3d", "whu_urban3d", "whu_railway3d",
        "whu_building", "osv", "whu_mix", "whu_3dbie_solarpv", "bijie_landslide",
        "maduo_earthquake_crack",
    },
}


OVERRIDES = {
    "sdnet2018": dict(
        persistent_id="10.15142/T3TD19; 10.1016/j.dib.2018.11.015",
        primary_url="https://doi.org/10.15142/T3TD19",
        license="CC BY 4.0 article; dataset terms on repository",
        public_asset_state="primary_record_verified",
        evidence_grade="Q2",
        verification_note="Corrects Gemini's unrelated Automation in Construction DOI.",
    ),
    "dacl": dict(
        canonical_name="dacl bridge-damage dataset family",
        aliases="dacl1k; dacl10k",
        primary_url="https://github.com/phiyodr/dacl10k-toolkit",
        persistent_id="10.5281/zenodo.8360303",
        public_asset_state="official_paper_and_toolkit_verified",
        evidence_grade="Q2",
        verification_note="dacl1k and dacl10k are version nodes; image overlap still needs Q3 hashes.",
    ),
    "codebrim": dict(
        canonical_name="CODEBRIM family",
        aliases="CODEBRIM; SegCODEBRIM",
        persistent_id="10.5281/zenodo.2620293; 10.5281/zenodo.10071534",
        primary_url="https://zenodo.org/records/2620293",
        public_asset_state="two_primary_records_verified",
        evidence_grade="Q2",
        verification_note="SegCODEBRIM reuses CODEBRIM images and adds crack masks; one family, two releases.",
    ),
    "metu_concrete_crack": dict(
        canonical_name="METU concrete-crack acquisition family",
        aliases="Concrete Crack Images for Classification; Concrete Crack Segmentation Dataset",
        persistent_id="10.17632/5y9wdsg2zt.2; 10.17632/jwsn7tfbrp.1",
        primary_url="https://data.mendeley.com/datasets/5y9wdsg2zt/2",
        public_asset_state="two_primary_records_verified",
        evidence_grade="Q2",
        verification_note="40,000 classification patches derive from 458 original images; segmentation is a separate release from the same acquisition family.",
    ),
    "mfnet": dict(
        eligibility_status="provisional",
        scope_fit="boundary_review",
        persistent_id="10.1109/IROS.2017.8206396",
        primary_url="https://doi.org/10.1109/IROS.2017.8206396",
        verification_note="Gemini DOI and LASNet-as-dataset-repository claims are wrong; urban-road labels fit modality but only weakly fit engineering inspection.",
    ),
    "kaist_multispectral": dict(
        eligibility_status="provisional",
        scope_fit="boundary_review",
        verification_note="Paired RGB-T is strong, but pedestrian-only semantics are outside urban-asset inspection unless the Cluster B scope is widened.",
    ),
    "flir_adas": dict(eligibility_status="provisional", scope_fit="boundary_review", verification_note="Original RGB and thermal views are not aligned; aligned community derivatives require separate version treatment."),
    "m3fd": dict(eligibility_status="provisional", scope_fit="boundary_review", verification_note="Paired modality verified in literature; dominant targets are generic road users rather than engineering assets."),
    "llvip": dict(eligibility_status="provisional", scope_fit="boundary_review", verification_note="Strictly paired low-light pedestrian data; engineering-asset semantics are absent."),
    "s2ds": dict(
        eligibility_status="include",
        scope_fit="in_scope",
        aliases="Structural Defects Dataset",
        primary_url="https://github.com/ben-z-original/s2ds",
        public_asset_state="official_repository_verified",
        license="academic use only; redistribution prohibited",
        evidence_grade="Q2",
        verification_note="743 segmentation patches with seven classes; Gemini narrative omitted it from the formal registry.",
    ),
    "gyu_det": dict(
        canonical_name="GYU-DET",
        aliases="Multi-defect type beam bridge dataset",
        cluster="A",
        eligibility_status="include",
        scope_fit="in_scope",
        task_types="object detection",
        modality="2D RGB",
        release_span="2025",
        public_asset_state="primary_record_verified",
        license="CC BY 4.0",
        persistent_id="10.57760/sciencedb.19893",
        primary_url="https://www.scidb.cn/detail?dataSetId=68827df9f367442c8be0c283e60ed3b7",
        evidence_grade="Q2",
        verification_note="Primary ScienceDB release overrides the S2 report's decision based on a later commercial reseller post.",
    ),
    "ttd": dict(
        canonical_name="TACK Tunnel Data (TTD)",
        aliases="TTD",
        primary_url="https://huggingface.co/datasets/TACK-project/TACK_Tunnel_Data",
        persistent_id="arXiv:2512.14477",
        public_asset_state="official_huggingface_asset_verified",
        evidence_grade="Q2",
        verification_note="Three tunnel domains and 1,298 512x512 slices; Gemini's '3 image sets' is not a sample-count field.",
    ),
    "whu_building": dict(
        canonical_name="WHU Building Dataset family",
        aliases="WHU aerial building; satellite subdatasets; building change detection subdataset",
        primary_url="https://gpcv.whu.edu.cn/data/",
        public_asset_state="official_portal_verified",
        evidence_grade="Q2",
        verification_note="More than 1,400 km2 is the umbrella-family coverage; 8,188 tiles/~220k buildings describes the aerial Christchurch subdataset only.",
    ),
    "semanticbridge": dict(
        canonical_name="SemanticBridge / Bridge3D",
        aliases="Bridge 3D segmentation dataset",
        persistent_id="arXiv:2512.15369",
        primary_url="https://arxiv.org/abs/2512.15369",
        verification_note="Preprint identity verified; public release asset remains provisional.",
    ),
    "semantic_kitti": dict(
        eligibility_status="provisional",
        scope_fit="boundary_review",
        verification_note="Urban 3D perception benchmark, but driving-scene semantics weakly represent city physical examination.",
    ),
}


def merge_record(existing: dict, incoming: dict) -> dict:
    sources = set(existing["source_flags"].split(";")) | set(incoming["source_flags"].split(";"))
    sources.discard("")
    existing["source_flags"] = ";".join(sorted(sources))
    existing["source_count"] = str(len(sources))
    for field in FIELDS:
        if not existing.get(field) and incoming.get(field):
            existing[field] = incoming[field]
    return existing


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source2", type=Path, help="Path to S2 report containing one-line JSON objects")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    records: dict[str, dict] = {}
    for line in args.source2.read_text(encoding="utf-8").splitlines():
        if not line.startswith("{"):
            continue
        obj = json.loads(line)
        row = base_record(obj)
        key = row["family_key"]
        records[key] = merge_record(records[key], row) if key in records else row

    for row in ADDITIONS:
        key = row["family_key"]
        records[key] = merge_record(records[key], row) if key in records else row

    for source, keys in SOURCE_MENTIONS.items():
        for key in keys:
            if key not in records:
                raise KeyError(f"Source mention {source}:{key} has no registry record")
            sources = set(records[key]["source_flags"].split(";"))
            sources.add(source)
            records[key]["source_flags"] = ";".join(sorted(sources))
            records[key]["source_count"] = str(len(sources))

    for key, values in OVERRIDES.items():
        if key not in records:
            raise KeyError(f"Override {key} has no registry record")
        records[key].update(values)

    cluster_order = {"A": 0, "B": 1, "C": 2, "D": 3, "future_scope": 4, "excluded": 5}
    rows = sorted(records.values(), key=lambda row: (cluster_order.get(row["cluster"], 9), row["canonical_name"].casefold()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
