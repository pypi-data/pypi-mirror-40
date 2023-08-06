from cybox.core import Observable
from lxml import etree
import pycountry
from six import text_type
import stix
from stix.campaign import Campaign
from stix.coa import CourseOfAction
from stix.common.identity import Identity
from stix.common.kill_chains import KillChainPhase, KillChainPhaseReference
from stix.data_marking import MarkingSpecification, MarkingStructure
from stix.exploit_target import ExploitTarget
from stix.extensions.identity.ciq_identity_3_0 import CIQIdentity3_0Instance
from stix.extensions.malware.maec_4_1_malware import MAECInstance
import stix.extensions.marking.ais
from stix.extensions.marking.ais import AISMarkingStructure
from stix.extensions.marking.simple_marking import SimpleMarkingStructure
from stix.extensions.marking.terms_of_use_marking import \
    TermsOfUseMarkingStructure
from stix.extensions.marking.tlp import TLPMarkingStructure
from stix.extensions.test_mechanism.open_ioc_2010_test_mechanism import \
    OpenIOCTestMechanism
from stix.extensions.test_mechanism.snort_test_mechanism import \
    SnortTestMechanism
from stix.extensions.test_mechanism.yara_test_mechanism import \
    YaraTestMechanism
from stix.incident import Incident
from stix.indicator import Indicator
from stix.threat_actor import ThreatActor
from stix.ttp import TTP
from stixmarx import navigator

from stix2elevator.confidence import convert_confidence
from stix2elevator.convert_cybox import (convert_cybox_object,
                                         fix_cybox_relationships)
from stix2elevator.convert_pattern import (ComparisonExpressionForElevator,
                                           CompoundObservationExpressionForElevator,
                                           ParentheticalExpressionForElevator,
                                           UnconvertedTerm,
                                           add_to_observable_mappings,
                                           add_to_pattern_cache,
                                           convert_indicator_to_pattern,
                                           convert_observable_to_pattern,
                                           create_boolean_expression,
                                           fix_pattern,
                                           interatively_resolve_placeholder_refs,
                                           remove_pattern_objects)
from stix2elevator.ids import (add_id_value, exists_id_key,
                               exists_ids_with_no_1x_object,
                               generate_stix20_id, get_id_value, get_id_values,
                               record_ids)
from stix2elevator.options import error, get_option_value, info, warn
from stix2elevator.utils import (add_marking_map_entry,
                                 check_map_1x_markings_to_20,
                                 convert_controlled_vocabs_to_open_vocabs,
                                 convert_timestamp_of_stix_object,
                                 convert_timestamp_to_string, identifying_info,
                                 iterpath, map_1x_markings_to_20,
                                 map_vocabs_to_label, operation_on_path)
from stix2elevator.vocab_mappings import (ATTACK_MOTIVATION_MAP, COA_LABEL_MAP,
                                          INCIDENT_LABEL_MAP,
                                          INDICATOR_LABEL_MAP,
                                          MALWARE_LABELS_MAP,
                                          REPORT_LABELS_MAP, SECTORS_MAP,
                                          THREAT_ACTOR_LABEL_MAP,
                                          THREAT_ACTOR_SOPHISTICATION_MAP,
                                          TOOL_LABELS_MAP)

if stix.__version__ >= "1.2.0.0":
    from stix.report import Report

# collect kill chains
_KILL_CHAINS_PHASES = {}


def process_kill_chain(kc):
    for kcp in kc.kill_chain_phases:
        # Use object itself as key.
        if kcp.phase_id:
            _KILL_CHAINS_PHASES[kcp.phase_id] = {"kill_chain_name": kc.name, "phase_name": kcp.name}
        else:
            _KILL_CHAINS_PHASES[kcp] = {"kill_chain_name": kc.name, "phase_name": kcp.name}


#
# identities
#


# def get_simple_name_from_identity(identity, bundle_instance, sdo_instance):
#     if isinstance(identity, CIQIdentity3_0Instance):
#         handle_relationship_to_refs([identity], sdo_instance["id"], bundle_instance, "attributed-to")
#     else:
#         return identity.name


def get_identity_ref(identity, env, temp_marking_id=None, from_package=False):
    if identity.idref is not None:
        # fix reference later
        return identity.idref
    else:
        ident20 = convert_identity(identity, env, temp_marking_id=temp_marking_id, from_package=from_package)
        env.bundle_instance["objects"].append(ident20)
        return ident20["id"]


def process_information_source(information_source, so, env, temp_marking_id=None):
    if information_source:
        if information_source.identity is not None:
            so["created_by_ref"] = get_identity_ref(information_source.identity, env, temp_marking_id)
        else:
            so["created_by_ref"] = env.created_by_ref

        if so == env.bundle_instance:
            warn("Information Source on %s is not representable in STIX 2.0", 401, so["id"])
        else:
            if information_source.description:
                process_description_and_short_description(so, information_source)
            if information_source.references:
                for ref in information_source.references:
                    so["external_references"].append({"source_name": "unknown", "url": ref})
            if not get_option_value("no_squirrel_gaps") and information_source.roles:
                for role in information_source.roles:
                    # no vocab to make to in 2.0
                    so["description"] += "\n\n" + "INFORMATION SOURCE ROLE: " + role.value
            if information_source.tools:
                for tool in information_source.tools:
                    add_tool_property_to_description(so, tool)
    else:
        so["created_by_ref"] = env.created_by_ref
    return so["created_by_ref"]


def convert_to_open_vocabs(stix20_obj, stix20_property_name, value, vocab_mapping):
    stix20_obj[stix20_property_name].append(map_vocabs_to_label(value, vocab_mapping))


def process_structured_text_list(text_list):
    full_text = ""
    for text_obj in text_list.sorted:
        full_text += text_obj.value
    return full_text


def process_description_and_short_description(so, entity, parent_info=False):
    if hasattr(entity, "descriptions") and entity.descriptions is not None:
        description_as_text = text_type(process_structured_text_list(entity.descriptions))
        if description_as_text:
            if parent_info:
                if not get_option_value("no_squirrel_gaps"):
                    if so["description"]:
                        so["description"] += "\nPARENT_DESCRIPTION: \n" + description_as_text
                    else:
                        so["description"] += description_as_text
            else:
                so["description"] += description_as_text
        if (not get_option_value("no_squirrel_gaps") and
                hasattr(entity, "short_descriptions") and
                entity.short_descriptions is not None):
            short_description_as_text = process_structured_text_list(entity.short_descriptions)
            if short_description_as_text:
                warn("The Short_Description property is no longer supported in STIX. The text was appended to the description property of %s", 301, so["id"])
                if parent_info:
                    if so["description"]:
                        so["description"] += "\nPARENT_SHORT_DESCRIPTION: \n" + short_description_as_text
                    else:
                        so["description"] += short_description_as_text
                else:
                    so["description"] += short_description_as_text
    # could be descriptionS or description
    elif hasattr(entity, "description") and entity.description is not None:
        so["description"] += text_type(entity.description.value)
    elif not get_option_value("no_squirrel_gaps") and hasattr(entity, "short_descriptions") and entity.short_descriptions is not None:
        so["description"] = text_type(process_structured_text_list(entity.short_descriptions))


def create_basic_object(stix20_type, stix1x_obj, env, parent_id=None, id_used=False):
    instance = {"type": stix20_type}
    if get_option_value("spec_version") == "2.1":
        instance["spec_version"] = "2.1"
    instance["id"] = generate_stix20_id(stix20_type, stix1x_obj.id_ if (stix1x_obj and
                                                                        hasattr(stix1x_obj, "id_") and
                                                                        stix1x_obj.id_) else parent_id, id_used)
    timestamp = convert_timestamp_of_stix_object(stix1x_obj, env.timestamp, True)
    instance["created"] = timestamp
    # may need to revisit if we handle 1.x versioning.
    instance["modified"] = timestamp
    instance["description"] = ""
    instance["external_references"] = []
    return instance


def convert_marking_specification(marking_specification, env):
    return_obj = []

    if marking_specification.marking_structures is not None:
        ms = marking_specification.marking_structures
        for mark_spec in ms:
            if mark_spec.idref or mark_spec.__class__.__name__ == "MarkingStructure":
                if not check_map_1x_markings_to_20(mark_spec):
                    # Don't print message multiple times if idref has been resolved.
                    warn("Could not resolve Marking Structure. Skipped object %s", 425, identifying_info(mark_spec))
                # Skip empty markings or ones that use the idref approach.
                continue

            marking_definition_instance = create_basic_object("marking-definition", mark_spec, env)
            process_information_source(marking_specification.information_source,
                                       marking_definition_instance,
                                       env,
                                       temp_marking_id=marking_definition_instance["id"])

            if "modified" in marking_definition_instance:
                del marking_definition_instance["modified"]

            if isinstance(mark_spec, TLPMarkingStructure):
                marking_definition_instance["definition_type"] = "tlp"
                definition = {}
                if mark_spec.color is not None:
                    definition["tlp"] = text_type(mark_spec.color)
                marking_definition_instance["definition"] = definition
            elif isinstance(mark_spec, TermsOfUseMarkingStructure):
                marking_definition_instance["definition_type"] = "statement"
                definition = {}
                if mark_spec.terms_of_use is not None:
                    definition["statement"] = text_type(mark_spec.terms_of_use)
                marking_definition_instance["definition"] = definition
            elif isinstance(mark_spec, SimpleMarkingStructure):
                marking_definition_instance["definition_type"] = "statement"
                definition = {}
                if mark_spec.statement is not None:
                    definition["statement"] = text_type(mark_spec.statement)
                marking_definition_instance["definition"] = definition
            elif isinstance(mark_spec, AISMarkingStructure):
                marking_definition_instance["definition_type"] = "ais"
                definition = {}
                if mark_spec.is_proprietary is not None:
                    definition["is_proprietary"] = "true"
                    if (mark_spec.is_proprietary.ais_consent is not None and
                            mark_spec.is_proprietary.ais_consent.consent is not None):
                        definition["consent"] = text_type(mark_spec.is_proprietary.ais_consent.consent).lower()
                    if (mark_spec.is_proprietary.tlp_marking is not None and
                            mark_spec.is_proprietary.tlp_marking.color is not None):
                        definition["tlp"] = text_type(mark_spec.is_proprietary.tlp_marking.color).lower()
                    if mark_spec.is_proprietary.cisa_proprietary is not None:
                        definition["is_cisa_proprietary"] = text_type(mark_spec.is_proprietary.cisa_proprietary).lower()
                elif mark_spec.not_proprietary is not None:
                    definition["is_proprietary"] = "false"
                    if (mark_spec.not_proprietary.ais_consent is not None and
                            mark_spec.not_proprietary.ais_consent.consent is not None):
                        definition["consent"] = text_type(mark_spec.not_proprietary.ais_consent.consent).lower()
                    if (mark_spec.not_proprietary.tlp_marking is not None and
                            mark_spec.not_proprietary.tlp_marking.color is not None):
                        definition["tlp"] = text_type(mark_spec.not_proprietary.tlp_marking.color).lower()
                    if mark_spec.not_proprietary.cisa_proprietary is not None:
                        definition["is_cisa_proprietary"] = text_type(mark_spec.not_proprietary.cisa_proprietary).lower()
                marking_definition_instance["definition"] = definition
            else:
                if mark_spec.__class__.__name__ in get_option_value("markings_allowed"):
                    warn("Could not resolve Marking Structure %s", 425, identifying_info(mark_spec))
                else:
                    error("Could not resolve Marking Structure %s", 425, identifying_info(mark_spec))
                    raise NameError("Could not resolve Marking Structure %s" % identifying_info(mark_spec))

            if "definition_type" in marking_definition_instance:
                val = add_marking_map_entry(mark_spec, marking_definition_instance["id"])
                info("Created Marking Structure for %s", 212, identifying_info(mark_spec))
                if val is not None and not isinstance(val, MarkingStructure):
                    info("Found same marking structure %s, using %s", 625, identifying_info(marking_specification), val)
                else:
                    finish_basic_object(marking_specification.id_, marking_definition_instance, env, mark_spec)
                    return_obj.append(marking_definition_instance)

    return return_obj


def finish_basic_object(old_id, instance, env, stix1x_obj, temp_marking_id=None):
    if old_id is not None:
        record_ids(old_id, instance["id"])
    if hasattr(stix1x_obj, "related_packages") and stix1x_obj.related_packages is not None:
        for p in stix1x_obj.related_packages:
            warn("Related_Packages type in %s not supported in STIX 2.0", 402, stix1x_obj.id_)

    # Attach markings to SDO if present.
    container = get_option_value("marking_container")
    markings = container.get_markings(stix1x_obj)
    object_marking_refs = []
    for marking in markings:
        for marking_spec in marking.marking_structures:
            stix20_marking = map_1x_markings_to_20(marking_spec)
            if (not isinstance(stix20_marking, MarkingStructure) and
                    instance["id"] != stix20_marking and
                    stix20_marking not in object_marking_refs):
                object_marking_refs.append(stix20_marking)
            elif temp_marking_id:
                object_marking_refs.append(temp_marking_id)
            elif not check_map_1x_markings_to_20(marking_spec):
                stix20_markings = convert_marking_specification(marking, env)
                env.bundle_instance["objects"].extend(stix20_markings)
                for m in stix20_markings:
                    if instance["id"] != m["id"] and m["id"] not in object_marking_refs:
                        object_marking_refs.append(m["id"])

    if object_marking_refs:
        instance["object_marking_refs"] = object_marking_refs

#
# handle gaps
#


def add_string_property_to_description(sdo_instance, property_name, property_value, is_list=False):
    if not get_option_value("no_squirrel_gaps") and property_value:
        if is_list:
            sdo_instance["description"] += "\n\n" + property_name.upper() + ":\n"
            property_values = []
            for v in property_value:
                property_values.append(text_type(v))
            sdo_instance["description"] += ",\n".join(property_values)
        else:
            sdo_instance["description"] += "\n\n" + property_name.upper() + ":\n\t" + text_type(property_value)
        warn("Appended %s to description of %s", 302, property_name, sdo_instance["id"])


def add_confidence_property_to_description(sdo_instance, confidence):
    if not get_option_value("no_squirrel_gaps"):
        if confidence is not None:
            sdo_instance["description"] += "\n\n" + "CONFIDENCE: "
            if confidence.value is not None:
                sdo_instance["description"] += text_type(confidence.value)
            if confidence.description is not None:
                sdo_instance["description"] += "\n\tDESCRIPTION: " + text_type(confidence.description)
            warn("Appended Confidence type content to description of %s", 304, sdo_instance["id"])


def add_statement_type_to_description(sdo_instance, statement, property_name):
    if statement and not get_option_value("no_squirrel_gaps"):
        sdo_instance["description"] += "\n\n" + property_name.upper() + ":"
        if statement.value:
            sdo_instance["description"] += text_type(statement.value)
        if statement.descriptions:
            descriptions = []
            for d in statement.descriptions:
                descriptions.append(text_type(d.value))
            sdo_instance["description"] += "\n\n\t".join(descriptions)

        if statement.source is not None:
            # FIXME: Handle source
            info("Source in %s is not handled, yet.", 815, sdo_instance["id"])
        if statement.confidence:
            add_confidence_property_to_description(sdo_instance, statement.confidence)
        warn("Appended Statement type content to description of %s", 305, sdo_instance["id"])


def add_multiple_statement_types_to_description(sdo_instance, statements, property_name):
    if not get_option_value("no_squirrel_gaps"):
        for s in statements:
            add_statement_type_to_description(sdo_instance, s, property_name)


def add_tool_property_to_description(sdo_instance, tool):
    if not get_option_value("no_squirrel_gaps"):
        sdo_instance["description"] += "\n\nTOOL SOURCE:"
        if tool.name:
            sdo_instance["description"] += "\n\tname: " + text_type(tool.name)
        warn("Appended Tool type content to description of %s", 306, sdo_instance["id"])

# Sightings


def handle_sightings_observables(related_observables, bundle_instance, parent_timestamp, sighted_object_created_by_ref):
    refs = []
    for ref in related_observables:
        if ref.item.idref is None:
            # embedded
            new20s = handle_embedded_object(ref.item, bundle_instance, sighted_object_created_by_ref, parent_timestamp)
            for new20 in new20s:
                refs.append(new20["id"])
        else:
            refs.append(ref.item.idref)
    return refs


def process_information_source_for_sighting(information_source, sighting_instance, bundle_instance, parent_timestamp):
    if information_source:
        if information_source.identity is not None:
            sighting_instance["where_sighted_refs"] = [get_identity_ref(information_source.identity, bundle_instance, parent_timestamp)]
            if information_source.description:
                process_description_and_short_description(sighting_instance, information_source)
            if information_source.references:
                for ref in information_source.references:
                    sighting_instance["external_references"].append({"url": ref})
            if not get_option_value("no_squirrel_gaps") and information_source.roles:
                for role in information_source.roles:
                    # no vocab to make to in 2.0
                    sighting_instance["description"] += "\n\n" + "INFORMATION SOURCE ROLE: " + role.value
            if information_source.tools:
                for tool in information_source.tools:
                    add_tool_property_to_description(sighting_instance, tool)


def handle_sighting(sighting, sighted_object_id, env):
    sighting_instance = create_basic_object("sighting", sighting, env)
    sighting_instance["count"] = 1
    sighting_instance["sighting_of_ref"] = sighted_object_id
    if sighting.related_observables:
        sighting_instance["observed_data_refs"] = handle_sightings_observables(sighting.related_observables, env)

    if sighting.source:
        process_information_source_for_sighting(sighting.source, sighting_instance, env)
    # assumption is that the observation is a singular, not a summary of observations
    sighting_instance["summary"] = False
    return sighting_instance


# Relationships


def create_relationship(source_ref, target_ref, env, verb, rel_obj=None):
    relationship_instance = create_basic_object("relationship", rel_obj, env)
    relationship_instance["source_ref"] = source_ref
    relationship_instance["target_ref"] = target_ref
    relationship_instance["relationship_type"] = verb
    relationship_instance["created_by_ref"] = env.created_by_ref
    if rel_obj is not None and hasattr(rel_obj, "relationship") and rel_obj.relationship is not None:
        relationship_instance["description"] = rel_obj.relationship.value
    return relationship_instance


# Creating and Linking up relationships  (three cases)
# 1.  The object is embedded - create the object, add it to the bundle, return to id so the relationship is complete
# 2.  an idref is given, and it has a corresponding 2.0 id, use it
# 3.  an idref is given, but it has NO corresponding 2.0 id, add 1.x id, and fix at the end in fix_relationships


def handle_relationship_to_objs(items, source_id, env, verb):
    for item in items:
        new20s = handle_embedded_object(item, env)
        for new20 in new20s:
            env.bundle_instance["relationships"].append(create_relationship(source_id,
                                                                            new20["id"] if new20 else None,
                                                                            env,
                                                                            verb,
                                                                            item))


def handle_relationship_to_refs(refs, source_id, env, verb, source_identity_ref=None):
    for ref in refs:
        if ref.item.idref is None:
            # embedded
            new20s = handle_embedded_object(ref.item, env)
            for new20 in new20s:
                env.bundle_instance["relationships"].append(create_relationship(source_id,
                                                                                new20["id"] if new20 else None,
                                                                                env,
                                                                                verb,
                                                                                ref))
        elif exists_id_key(ref.item.idref):
            for to_ref in get_id_value(ref.item.idref):
                env.bundle_instance["relationships"].append(create_relationship(source_id,
                                                                                to_ref,
                                                                                env,
                                                                                verb,
                                                                                ref))
        else:
            # a forward reference, fix later
            env.bundle_instance["relationships"].append(create_relationship(source_id,
                                                                            ref.item.idref,
                                                                            env,
                                                                            verb,
                                                                            ref))


def handle_relationship_from_refs(refs, target_id, env, verb):
    for ref in refs:
        if ref.item.idref is None:
            # embedded
            new20s = handle_embedded_object(ref.item, env)
            for new20 in new20s:
                env.bundle_instance["relationships"].append(create_relationship(new20["id"] if new20 else None,
                                                                                target_id,
                                                                                env,
                                                                                verb,
                                                                                ref))
        elif exists_id_key(ref.item.idref):
            for from_ref in get_id_value(ref.item.idref):
                env.bundle_instance["relationships"].append(create_relationship(from_ref,
                                                                                target_id,
                                                                                env,
                                                                                verb,
                                                                                ref))
        else:
            # a forward reference, fix later
            env.bundle_instance["relationships"].append(create_relationship(ref.item.idref,
                                                                            target_id,
                                                                            env,
                                                                            verb,
                                                                            ref))


def reference_needs_fixing(ref):
    return ref and ref.find("--") == -1


def determine_appropriate_verb(current_verb, m_id):
    if m_id is not None and current_verb == "uses":
        type_and_uuid = m_id.split("--")
        if type_and_uuid[0] == "identity":
            return "targets"
    return current_verb


# for ids in source and target refs that are still 1.x ids,
def fix_relationships(relationships, bundle_instance):
    for ref in relationships:
        if reference_needs_fixing(ref["source_ref"]):
            if not exists_id_key(ref["source_ref"]):
                new_id = generate_stix20_id(None, str.lower(ref["source_ref"]))
                if new_id is None:
                    warn("Dangling source reference %s in %s", 601, ref["source_ref"], ref["id"])
                add_id_value(ref["source_ref"], new_id)
            mapped_ids = get_id_value(ref["source_ref"])
            if mapped_ids[0] is None:
                warn("Dangling source reference %s in %s", 601, ref["source_ref"], ref["id"])
            first_one = True
            for m_id in mapped_ids:
                if first_one:
                    ref["source_ref"] = m_id
                else:
                    bundle_instance["relationships"].append(create_relationship(m_id, ref["target_ref"], ref["verb"]))
        if reference_needs_fixing(ref["target_ref"]):
            if not exists_id_key(ref["target_ref"]):
                new_id = generate_stix20_id(None, str.lower(ref["target_ref"]))
                if new_id is None:
                    warn("Dangling target reference %s in %s", 602, ref["target_ref"], ref["id"])
                add_id_value(ref["target_ref"], new_id)
            mapped_ids = get_id_value(ref["target_ref"])
            if mapped_ids[0] is None:
                warn("Dangling target reference %s in %s", 602, ref["target_ref"], ref["id"])
            first_one = True
            for m_id in mapped_ids:
                verb = determine_appropriate_verb(ref["relationship_type"], m_id)
                if first_one:
                    ref["target_ref"] = m_id
                    ref["relationship_type"] = verb
                else:
                    bundle_instance["relationships"].append(create_relationship(ref["source_ref"], m_id, verb))


# Relationships are not in 1.x, so they must be added explicitly to reports.
# This is done after the package has been processed, and the relationships are "fixed", so all relationships are known
#
# For each report:
#   For each relationship
#       if the source and target are part of the report, add the relationship
#       if the source is part of the report, add the relationship AND then the target,
#          UNLESS the target ref is "dangling"
#       if the target is part of the report, add the relationship AND then the source,
#          UNLESS the source ref is "dangling"


def add_relationships_to_reports(bundle_instance):
    rels_to_include = []
    new_ids = get_id_values()
    for rep in bundle_instance["reports"]:
        refs_in_this_report = rep["object_refs"]
        for rel in bundle_instance["relationships"]:
            if (("source_ref" in rel and rel["source_ref"] in refs_in_this_report) and
                    ("target_ref" in rel and rel["target_ref"] in refs_in_this_report)):
                rels_to_include.append(rel["id"])
            elif "source_ref" in rel and rel["source_ref"] in refs_in_this_report:
                # and target_ref is not in refs_in_this_report
                if "target_ref" in rel and rel["target_ref"] and (
                        rel["target_ref"] in new_ids or exists_ids_with_no_1x_object(rel["target_ref"])):
                    rels_to_include.append(rel["id"])
                    rels_to_include.append(rel["target_ref"])
                    warn("Including %s in %s and added the target_ref %s to the report", 704, rel["id"], rep["id"], rel["target_ref"])
                elif not ("target_ref" in rel and rel["target_ref"]):
                    rels_to_include.append(rel["id"])
                    warn("Including %s in %s although the target_ref is unknown", 706, rel["id"], rep["id"])
                elif not (rel["target_ref"] in new_ids or exists_ids_with_no_1x_object(rel["target_ref"])):
                    warn("Not including %s in %s because there is no corresponding SDO for %s", 708, rel["id"], rep["id"], rel["target_ref"])
            elif "target_ref" in rel and rel["target_ref"] in refs_in_this_report:
                if "source_ref" in rel and rel["source_ref"] and (
                        rel["source_ref"] in new_ids or exists_ids_with_no_1x_object(rel["source_ref"])):
                    rels_to_include.append(rel["id"])
                    rels_to_include.append(rel["source_ref"])
                    warn("Including %s in %s and added the source_ref %s to the report", 705, rel["id"], rep["id"], rel["source_ref"])
                elif not ("source_ref" in rel and rel["source_ref"]):
                    rels_to_include.append(rel["id"])
                    warn("Including %s in %s although the source_ref is unknown", 707, rel["id"], rep["id"])
                elif not (rel["source_ref"] in new_ids or exists_ids_with_no_1x_object(rel["source_ref"])):
                    warn("Not including %s in %s because there is no corresponding SDO for %s", 709, rel["id"], rep["id"], rel["source_ref"])
        if "object_refs" in rep:
            rep["object_refs"].extend(rels_to_include)
        else:
            rep["object_refs"] = rels_to_include


# confidence

def add_confidence_to_object(sdo_instance, confidence):
    if confidence is not None:
        sdo_instance["confidence"] = convert_confidence(confidence, id)


# campaign


def convert_campaign(camp, env):
    campaign_instance = create_basic_object("campaign", camp, env)
    process_description_and_short_description(campaign_instance, camp)
    campaign_instance["name"] = camp.title
    if camp.names is not None:
        campaign_instance["aliases"] = []
        for name in camp.names:
            if isinstance(name, text_type):
                campaign_instance["aliases"].append(name)
            else:
                campaign_instance["aliases"].append(name.value)
    if "created_by_ref" in campaign_instance:
        new_env = env.newEnv(timestamp=campaign_instance["created"], created_by_ref=campaign_instance["created_by_ref"])
    else:
        new_env = env.newEnv(timestamp=campaign_instance["created"])
    # process information source before any relationships
    new_env.add_to_env(created_by_ref=process_information_source(camp.information_source, campaign_instance, new_env))

    add_multiple_statement_types_to_description(campaign_instance, camp.intended_effects, "intended_effect")
    add_string_property_to_description(campaign_instance, "status", camp.status)

    if get_option_value("spec_version") == "2.0":
        add_confidence_property_to_description(campaign_instance, camp.confidence)
    else:  # 2.1
        add_confidence_to_object(campaign_instance, camp.confidence)

    if camp.activity is not None:
        for a in camp.activity:
            warn("Campaign/Activity type in %s not supported in STIX 2.0", 403, campaign_instance["id"])
    if camp.related_ttps is not None:
        # victims use targets, not uses
        handle_relationship_to_refs(camp.related_ttps,
                                    campaign_instance["id"],
                                    new_env,
                                    "uses")
    if camp.related_incidents is not None:
        handle_relationship_from_refs(camp.related_incidents,
                                      campaign_instance["id"],
                                      new_env,
                                      "attributed-to")
    if camp.related_indicators is not None:
        handle_relationship_from_refs(camp.related_indicators,
                                      campaign_instance["id"],
                                      new_env,
                                      "indicates")
    if camp.attribution is not None:
        for att in camp.attribution:
            handle_relationship_to_refs(att,
                                        campaign_instance["id"],
                                        new_env,
                                        "attributed-to")
    if camp.associated_campaigns:
        warn("All associated campaigns relationships of %s are assumed to not represent STIX 1.2 versioning", 710, camp.id_)
        handle_relationship_to_refs(camp.related_coas,
                                    campaign_instance["id"],
                                    new_env,
                                    "related-to")
    finish_basic_object(camp.id_, campaign_instance, env, camp)
    return campaign_instance


# course of action


def add_objective_property_to_description(sdo_instance, objective):
    if not get_option_value("no_squirrel_gaps"):
        if objective is not None:
            sdo_instance["description"] += "\n\n" + "OBJECTIVE: "
            all_text = []

            if objective.descriptions:
                for d in objective.descriptions:
                    all_text.append(text_type(d.value))

            if objective.short_descriptions:
                for sd in objective.short_descriptions:
                    all_text.append(text_type(sd.value))

            sdo_instance["description"] += "\n\n\t".join(all_text)

            if objective.applicability_confidence:
                add_confidence_property_to_description(sdo_instance, objective.applicability_confidence)


def convert_course_of_action(coa, env):
    coa_instance = create_basic_object("course-of-action", coa, env)
    new_env = env.newEnv(timestamp=coa_instance["created"])
    process_description_and_short_description(coa_instance, coa)
    coa_instance["name"] = coa.title
    add_string_property_to_description(coa_instance, "stage", coa.stage)
    if coa.type_:
        convert_controlled_vocabs_to_open_vocabs(coa_instance, "labels", [coa.type_], COA_LABEL_MAP, False)
    add_objective_property_to_description(coa_instance, coa.objective)

    if coa.parameter_observables is not None:
        # parameter observables, maybe turn into pattern expressions and put in description???
        warn("Parameter Observables in %s are not handled, yet.", 814, coa_instance["id"])
    if coa.structured_coa:
        warn("Structured COAs type in %s are not supported in STIX 2.0", 404, coa_instance["id"])
    add_statement_type_to_description(coa_instance, coa.impact, "impact")
    add_statement_type_to_description(coa_instance, coa.cost, "cost")
    add_statement_type_to_description(coa_instance, coa.efficacy, "efficacy")
    coa_created_by_ref = process_information_source(coa.information_source,
                                                    coa_instance,
                                                    new_env)
    # process information source before any relationships
    if coa.related_coas:
        warn("All associated coas relationships of %s are assumed to not represent STIX 1.2 versioning", 710, coa.id_)
        handle_relationship_to_refs(coa.related_coas, coa_instance["id"], new_env,
                                    coa_created_by_ref, "related-to")
    finish_basic_object(coa.id_, coa_instance, env, coa)
    return coa_instance


# exploit target


def process_et_properties(sdo_instance, et, env):
    process_description_and_short_description(sdo_instance, et, True)
    if "name" in sdo_instance:
        info("Title %s used for name, appending exploit_target %s title in description property",
             303, sdo_instance["type"], sdo_instance["id"])
        add_string_property_to_description(sdo_instance, "title", et.title, False)
    elif et.title is not None:
        sdo_instance["name"] = et.title
    new_env = env.newEnv(timestamp=sdo_instance["created"])
    new_env.add_to_env(created_by_ref=process_information_source(et.information_source, sdo_instance, new_env))
    if et.potential_coas is not None:
        handle_relationship_from_refs(et.potential_coas, sdo_instance["id"],
                                      new_env,
                                      "mitigates")


def convert_vulnerability(v, et, env):
    vulnerability_instance = create_basic_object("vulnerability", v, env, et.id_)
    if v.title is not None:
        vulnerability_instance["name"] = v.title
    process_description_and_short_description(vulnerability_instance, v)
    if v.cve_id is not None:
        vulnerability_instance["external_references"].append({"source_name": "cve", "external_id": v.cve_id})
    if v.osvdb_id is not None:
        vulnerability_instance["external_references"].append({"source_name": "osvdb", "external_id": v.osvdb_id})

    if v.source is not None:
        add_string_property_to_description(vulnerability_instance, "source", v.source, False)

    if v.cvss_score is not None:
        # FIXME: add CVSS score into description
        info("CVSS Score in %s is not handled, yet.", 815, vulnerability_instance["id"])

    if v.discovered_datetime is not None:
        add_string_property_to_description(vulnerability_instance,
                                           "discovered_datetime",
                                           v.discovered_datetime.value.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                           False)

    if v.published_datetime is not None:
        add_string_property_to_description(vulnerability_instance,
                                           "published_datetime",
                                           v.published_datetime.value.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                           False)

    if v.affected_software is not None:
        info("Affected Software in %s is not handled, yet.", 815, vulnerability_instance["id"])

    if v.references is not None:
        for ref in v.references:
            vulnerability_instance["external_references"].append({"source_name": "internet_resource", "url": ref.reference})
    process_et_properties(vulnerability_instance, et, env)
    finish_basic_object(et.id_, vulnerability_instance, env, v)
    return vulnerability_instance


def convert_exploit_target(et, env):
    ets = []
    if hasattr(et, "timestamp") and et.timestamp:
        new_env = env.newEnv(timestamp=et.timestamp)
    else:
        new_env = env
    if et.vulnerabilities is not None:
        for v in et.vulnerabilities:
            ets.append(convert_vulnerability(v, et, new_env))
    if et.weaknesses is not None:
        for w in et.weaknesses:
            warn("ExploitTarget/Weaknesses type in %s not supported in STIX 2.0", 405, et.id_)
    if et.configuration is not None:
        for c in et.configuration:
            warn("ExploitTarget/Configurations type in %s not supported in STIX 2.0", 406, et.id_)
    env.bundle_instance["objects"].extend(ets)
    return ets


# identities

def get_name(name):
    return name.name_elements[0].value


def convert_party_name(party_name, obj, is_identity_obj):
    if party_name.organisation_names and party_name.person_names:
        error("Identity %s has organization and person names", 606, obj["id"])
    if party_name.person_names:
        if is_identity_obj:
            obj["identity_class"] = "individual"
        first_one = True
        for name in party_name.person_names:
            if first_one:
                obj["name"] = get_name(name)
                first_one = False
            else:
                warn("Only one person name allowed for %s in STIX 2.0, used first one", 502, obj["id"])
                # add to description
    elif party_name.organisation_names:
        if is_identity_obj:
            obj["identity_class"] = "organization"
        first_one = True
        for name in party_name.organisation_names:
            if first_one:
                obj["name"] = get_name(name)
                first_one = False
            else:
                warn("Only one organization name allowed for %s in STIX 2.0, used first one", 503, obj["id"])
                # add to description


_LOCATIONS = {}


def determine_country_code(geo):
    if geo.name_code:
        return geo.name_code
    else:
        iso = pycountry.countries.get(name=geo.value)
        if iso:
            return iso.alpha_2
        else:
            if geo.value:
                warn("No ISO code for %s, therefore using full name", 618, geo.value)
                return geo.value
            else:
                return None


# spec doesn't indicate that code is preferred
def determine_aa(geo):
    if geo.name_code:
        return geo.name_code
    elif geo.value:
        return geo.value
    else:
        return None


def convert_ciq_addresses2_1(ciq_info_addresses, identity_instance, env, parent_id=None):
    location_keys = []
    for add in ciq_info_addresses:
        if not add.free_text_address:
            # only reuse if administrative area and country match, and no free text address
            if hasattr(add, "administrative_area") and add.administrative_area and hasattr(add,
                                                                                           "country") and add.country:
                if len(add.country.name_elements) == 1:
                    cc = determine_country_code(add.country.name_elements[0])
                    for aa in add.administrative_area.name_elements:
                        location_keys.append("c:" + text_type(cc) +
                                             "," +
                                             "aa:" + text_type(determine_aa(aa)))
                else:
                    warn("Multiple administrative areas with multiple countries in %s is not handled", 631, None)
            elif hasattr(add, "administrative_area") and add.administrative_area:
                for aa in add.adminstrative_area.name_elements:
                    location_keys.append("aa:" + text_type(determine_aa(aa)))
            elif hasattr(add, "country") and add.country:
                for c in add.country.name_elements:
                    location_keys.append("c:" + text_type(determine_country_code(c)))
        else:
            # only remember locations with no free text address
            warn("Location with free text address in %s not handled yet", 433, identity_instance["id"])
        for key in location_keys:
            if key in _LOCATIONS:
                location = _LOCATIONS[key]
            else:
                aa = None
                c = None
                location = create_basic_object("location", add, env)
                location["spec_version"] = "2.1"
                if key.find(",") != -1:
                    both_parts = key.split(",")
                    c = both_parts[0].split(":")[1]
                    aa = both_parts[1].split(":")[1]
                else:
                    part = key.split(":")
                    if part[0] == "c":
                        c = part[1]
                    elif part[0] == "aa":
                        aa = part[1]
                if aa:
                    location["administrative_area"] = aa
                if c:
                    location["country"] = c
                _LOCATIONS[key] = location
                env.bundle_instance["objects"].append(location)
            env.bundle_instance["objects"].append(create_relationship(identity_instance["id"],
                                                                      location["id"],
                                                                      env,
                                                                      "located-at"))


def convert_identity(identity, env, parent_id=None, temp_marking_id=None, from_package=False):
    identity_instance = create_basic_object("identity", identity, env, parent_id)
    identity_instance["sectors"] = []
    identity_instance["identity_class"] = "unknown"
    if identity.name is not None:
        identity_instance["name"] = identity.name
    if isinstance(identity, CIQIdentity3_0Instance):
        if identity.roles:
            warn("Roles is not a property of an identity (%s).  Perhaps the roles are associated with a related Threat Actor",
                 428,
                 identity_instance["id"])
            # convert_controlled_vocabs_to_open_vocabs(identity_instance, "roles", identity.roles, ROLES_MAP, False)
        ciq_info = identity._specification
        if ciq_info.party_name:
            if "name" in identity_instance:
                warn("CIQ name found in %s, overriding other name", 711, identity_instance["id"])
            convert_party_name(ciq_info.party_name, identity_instance, True)
        if ciq_info.organisation_info:
            identity_instance["identity_class"] = "organization"
            warn("Based on CIQ information, %s is assumed to be an organization", 716, identity_instance["id"])
            if ciq_info.organisation_info.industry_type:
                industry = ciq_info.organisation_info.industry_type.replace(" ,", ",")
                industry = industry.replace(", ", ",")
                industry = industry.split(",")
                convert_controlled_vocabs_to_open_vocabs(identity_instance, "sectors", industry, SECTORS_MAP, False)
        if ciq_info.addresses:
            if get_option_value("spec_version") == "2.1":
                convert_ciq_addresses2_1(ciq_info.addresses, identity_instance, env, parent_id)
    if identity.related_identities:
        msg = "All associated identities relationships of %s are assumed to not represent STIX 1.2 versioning"
        warn(msg, 710, identity_instance["id"])
        handle_relationship_to_refs(identity.related_identities, identity_instance["id"], env, "related-to")
    finish_basic_object(identity.id_, identity_instance,
                        env.newEnv(created_by_ref=identity_instance["id"] if from_package else parent_id),
                        identity,
                        temp_marking_id=temp_marking_id)
    return identity_instance


# incident


def convert_incident(incident, env):
    incident_instance = create_basic_object("incident", incident, env)
    new_env = env.newEnv(timestamp=incident_instance["created"])
    process_description_and_short_description(incident_instance, incident)
    if incident.title is not None:
        incident_instance["name"] = incident.title
    if incident.external_ids is not None:
        for ex_id in incident.external_ids:
            incident_instance["external_references"].append(
                {"source_name": ex_id.external_id.source, "external_id": ex_id.external_id.value})
    # time
    if incident.categories is not None:
        convert_controlled_vocabs_to_open_vocabs(incident_instance, "labels", incident.categories, INCIDENT_LABEL_MAP,
                                                 False)
    # process information source before any relationships
    new_env.add_to_env(created_by_ref=process_information_source(incident.information_source, incident_instance, new_env))

    if get_option_value("spec_version") == "2.0":
        add_confidence_property_to_description(incident_instance, incident.confidence)
    else:  # 2.1
        add_confidence_to_object(incident_instance, incident.confidence)

    # process information source before any relationships
    if incident.related_indicators is not None:
        handle_relationship_from_refs(incident.related_indicators, incident_instance["id"], new_env, "indicates")
    if incident.related_observables is not None:
        handle_relationship_from_refs(incident.related_observables, incident_instance["id"], new_env, "part-of")
    if incident.leveraged_ttps is not None:
        warn("Using related-to for the leveraged TTPs of %s", 718, incident.id_)
        handle_relationship_to_refs(incident.leveraged_ttps, incident_instance["id"], new_env, "related-to")

    if incident.reporter is not None:
        # FIXME: add reporter to description
        info("Incident Reporter in %s is not handled, yet.", 815, incident_instance["id"])

    if incident.responders is not None:
        # FIXME: add responders to description
        info("Incident Responders in %s is not handled, yet.", 815, incident_instance["id"])

    if incident.coordinators is not None:
        # FIXME: add coordinators to description
        info("Incident Coordinators in %s is not handled, yet.", 815, incident_instance["id"])

    if incident.victims is not None:
        # FIXME: add victim to description
        info("Incident Victims in %s is not handled, yet.", 815, incident_instance["id"])

    if incident.affected_assets is not None:
        # FIXME: add affected_assets to description
        info("Incident Affected Assets in %s is not handled, yet.", 815, incident_instance["id"])

    if incident.impact_assessment is not None:
        # FIXME: add impact_assessment to description
        info("Incident Impact Assessment in %s is not handled, yet", 815, incident_instance["id"])
    add_string_property_to_description(incident_instance, "status", incident.status)
    if incident.related_incidents:
        warn("All associated incidents relationships of %s are assumed to not represent STIX 1.2 versioning",
             710, incident_instance["id"])
        handle_relationship_to_refs(incident.related_incidents, incident_instance["id"], new_env, "related-to")
    finish_basic_object(incident.id_, incident_instance, env, incident)
    return incident_instance


# indicator


def convert_kill_chains(kill_chain_phases, sdo_instance):
    if kill_chain_phases is not None:
        kill_chain_phases_20 = []
        for phase in kill_chain_phases:
            if isinstance(phase, KillChainPhaseReference):
                try:
                    if phase.phase_id:
                        kill_chain_info = _KILL_CHAINS_PHASES[phase.phase_id]
                    else:
                        kill_chain_info = _KILL_CHAINS_PHASES[phase]
                    kill_chain_phases_20.append({"kill_chain_name": kill_chain_info["kill_chain_name"],
                                                 "phase_name": kill_chain_info["phase_name"]})
                except KeyError:
                    kill_chain_phases_20.append(phase.phase_id)
            elif isinstance(phase, KillChainPhase):
                kill_chain_phases_20.append({"kill_chain_name": phase.kill_chain_name, "phase_name": phase.name})
        if kill_chain_phases_20:
            sdo_instance["kill_chain_phases"] = kill_chain_phases_20


_ALLOW_YARA_AND_SNORT_PATTENS = False


def convert_test_mechanism(indicator, indicator_instance):
    if indicator.test_mechanisms is not None:
        if not _ALLOW_YARA_AND_SNORT_PATTENS:
            warn("YARA/SNORT patterns on %s not supported in STIX 2.0", 504, indicator_instance["id"])
            return
        if hasattr(indicator_instance, "pattern"):
            # TODO: maybe put in description
            warn("Only one type pattern can be specified in %s - using cybox", 712, indicator_instance["id"])
        else:
            for tm in indicator.test_mechanisms:
                if hasattr(indicator_instance, "pattern"):
                    # TODO: maybe put in description
                    msg = "Only one alternative test mechanism allowed for %s in STIX 2.0 - used first one, which was %s"
                    warn(msg, 506, indicator_instance["id"], indicator_instance["pattern_lang"])
                else:
                    if isinstance(tm, YaraTestMechanism):

                        indicator_instance["pattern"] = text_type(tm.rule.value)
                        indicator_instance["pattern_lang"] = "yara"
                    elif isinstance(tm, SnortTestMechanism):
                        list_of_strings = []
                        for rule in tm.rules:
                            list_of_strings.append(text_type(rule.value))
                        indicator_instance["pattern"] = ", ".join(list_of_strings)
                        indicator_instance["pattern_lang"] = "snort"
                    elif isinstance(tm, OpenIOCTestMechanism):
                        indicator_instance["pattern"] = etree.tostring(tm.ioc)
                        indicator_instance["pattern_lang"] = "openioc"


def negate_indicator(indicator):
    return hasattr(indicator, "negate") and indicator.negate


def convert_indicator(indicator, env):
    indicator_instance = create_basic_object("indicator", indicator, env)
    new_env = env.newEnv(timestamp=indicator_instance["created"])
    process_description_and_short_description(indicator_instance, indicator)
    convert_controlled_vocabs_to_open_vocabs(indicator_instance,
                                             "labels" if get_option_value(
                                                 "spec_version") == "2.0" else "indicator_types",
                                             indicator.indicator_types,
                                             INDICATOR_LABEL_MAP, False)
    if indicator.title is not None:
        indicator_instance["name"] = indicator.title
    if indicator.alternative_id is not None:
        for alt_id in indicator.alternative_id:
            indicator_instance["external_references"].append({"source_name": "alternative_id", "external_id": alt_id})
    if indicator.valid_time_positions is not None:
        for window in indicator.valid_time_positions:
            if "valid_from" not in indicator_instance:
                if not window.start_time.value:
                    warn("No start time for the first valid time interval is available in %s, other time intervals might be more appropriate",
                         619, indicator_instance["id"])
                indicator_instance["valid_from"] = \
                    convert_timestamp_to_string(window.start_time.value, indicator_instance["created"])
                indicator_instance["valid_until"] = \
                    convert_timestamp_to_string(window.end_time.value, indicator_instance["created"])
            else:
                warn("Only one valid time window allowed for %s in STIX 2.0 - used first one",
                     507, indicator_instance["id"])
        if "valid_from" not in indicator_instance:
            warn("No valid time position information available in %s, using parent timestamp",
                 903, indicator_instance["id"])
            indicator_instance["valid_from"] = convert_timestamp_of_stix_object(indicator, env.timestamp)
    convert_kill_chains(indicator.kill_chain_phases, indicator_instance)
    if indicator.likely_impact:
        add_statement_type_to_description(indicator_instance, indicator.likely_impact, "likely_impact")

    if get_option_value("spec_version") == "2.0":
        add_confidence_property_to_description(indicator_instance, indicator.confidence)
    else:  # 2.1
        add_confidence_to_object(indicator_instance, indicator.confidence)
    if indicator.observable is not None:
        indicator_instance["pattern"] = convert_observable_to_pattern(indicator.observable)
        add_to_pattern_cache(indicator.id_, indicator_instance["pattern"])
    if indicator.composite_indicator_expression is not None:
        expressions = []
        if stix.__version__ >= "1.2.0.0":
            sub_indicators = indicator.composite_indicator_expression.indicator
        else:
            sub_indicators = indicator.composite_indicator_expression
        for ind in sub_indicators:
            term = convert_indicator_to_pattern(ind)
            if term:
                expressions.append(term)
        indicator_instance["pattern"] = create_boolean_expression(indicator.composite_indicator_expression.operator,
                                                                  expressions)
    if indicator.observable and indicator.composite_indicator_expression or indicator.composite_indicator_expression:
        warn("Indicator %s has an observable or indicator composite expression which may not supported \
correctly in STIX 2.0 - please check this pattern",
             407, indicator_instance["id"])
        # add_to_pattern_cache(indicator.id_, indicator_instance["pattern"])
    if "pattern" not in indicator_instance:
        # STIX doesn't handle multiple patterns for indicators
        convert_test_mechanism(indicator, indicator_instance)
    indicator_created_by_ref = process_information_source(indicator.producer, indicator_instance,
                                                          env.newEnv(timestamp=indicator_instance["created"]))
    # process information source before any relationships
    if indicator.sightings:
        for s in indicator.sightings:
            env.bundle_instance["objects"].append(handle_sighting(s, indicator_instance["id"], new_env))
    if indicator.suggested_coas is not None:
        warn("Using related-to for the suggested COAs of %s", 718, indicator.id_)
        handle_relationship_to_refs(indicator.suggested_coas, indicator_instance["id"], new_env,
                                    "related-to", indicator_created_by_ref)
    if indicator.related_campaigns is not None:
        handle_relationship_to_refs(indicator.related_campaigns, indicator_instance["id"], new_env,
                                    "attributed-to", indicator_created_by_ref)
    if indicator.indicated_ttps is not None:
        handle_relationship_to_refs(indicator.indicated_ttps, indicator_instance["id"], new_env,
                                    "indicates", indicator_created_by_ref)
    if indicator.related_indicators:
        warn("All associated indicators relationships of %s are assumed to not represent STIX 1.2 versioning", 710, indicator.id_)
        handle_relationship_to_refs(indicator.related_indicators, indicator_instance["id"], new_env,
                                    "related-to", indicator_created_by_ref)
    finish_basic_object(indicator.id_, indicator_instance, env, indicator)
    return indicator_instance


# observables


def convert_observed_data(obs, env):
    observed_data_instance = create_basic_object("observed-data", obs, env)
    observed_data_instance["objects"] = convert_cybox_object(obs.object_)
    if obs.object_.related_objects:
        for o in obs.object_.related_objects:
            # create index for stix 2.0 cyber observable
            current_largest_id = max(observed_data_instance["objects"].keys())
            related = convert_cybox_object(o)
            if related:
                for index, obj in related.items():
                    observed_data_instance["objects"][text_type(int(index) + int(current_largest_id) + 1)] = obj
    info("'first_observed' and 'last_observed' data not available directly on %s - using timestamp", 901, obs.id_)
    observed_data_instance["first_observed"] = observed_data_instance["created"]
    observed_data_instance["last_observed"] = observed_data_instance["created"]
    observed_data_instance["number_observed"] = 1 if obs.sighting_count is None else obs.sighting_count
    # created_by
    finish_basic_object(obs.id_, observed_data_instance, env, obs)
    # remember the original 1.x observable, in case it has to be turned into a pattern later
    add_to_observable_mappings(obs)
    return observed_data_instance


# report


def process_report_contents(report, env, report_instance):
    report_instance["object_refs"] = []
    # campaigns
    if report.campaigns:
        for camp in report.campaigns:
            if camp.id_ is not None:
                camp20 = convert_campaign(camp, env)
                env.bundle_instance["objects"].append(camp20)
                report_instance["object_refs"].append(camp20["id"])
            else:
                report_instance["object_refs"].append(camp.idref)

    # coas
    if report.courses_of_action:
        for coa in report.courses_of_action:
            if coa.id_ is not None:
                coa20 = convert_course_of_action(coa, env)
                env.bundle_instance["objects"].append(coa20)
                report_instance["object_refs"].append(coa20["id"])
            else:
                report_instance["object_refs"].append(coa.idref)

    # exploit-targets
    if report.exploit_targets:
        for et in report.exploit_targets:
            convert_exploit_target(et, env)

    # incidents
    if get_option_value("incidents"):
        if report.incidents:
            for i in report.incidents:
                if i.id_ is not None:
                    i20 = convert_incident(i, env)
                    env.bundle_instance["incidents"].append(i20)
                    report_instance["object_refs"].append(i20["id"])
                else:
                    report_instance["object_refs"].append(i.idref)

    # indicators
    if report.indicators:
        for i in report.indicators:
            if i.id_ is not None:
                i20 = convert_indicator(i, env)
                env.bundle_instance["indicators"].append(i20)
                report_instance["object_refs"].append(i20["id"])
            else:
                report_instance["object_refs"].append(i.idref)

    # locations
    # if report.locations:
    #     for l in report.locations:
    #             if i.id_ is not None:
    #                 i20 = convert_indicator(i, env)
    #                 env.bundle_instance["indicators"].append(i20)
    #                 report_instance["object_refs"].append(i20["id"])
    #             else:
    #                 report_instance["object_refs"].append(i.idref)

    # observables
    if report.observables:
        for o_d in report.observables:
            if o_d.id_ is not None:
                o_d20 = convert_observed_data(o_d, env)
                env.bundle_instance["observed_data"].append(o_d20)
                report_instance["object_refs"].append(o_d20["id"])
            else:
                report_instance["object_refs"].append(o_d.idref)

    # threat actors
    if report.threat_actors:
        for ta in report.threat_actors:
            if ta.id_ is not None:
                ta20 = convert_threat_actor(ta, env)
                env.bundle_instance["objects"].append(ta20)
                report_instance["object_refs"].append(ta20["id"])
            else:
                report_instance["object_refs"].append(ta.idref)

    # ttps
    if report.ttps:
        for ttp in report.ttps:
            if ttp.id_:
                ttps20 = convert_ttp(ttp, env)
                for ttp20 in ttps20:
                    if ttp20["type"] == "malware":
                        env.bundle_instance["objects"].append(ttp)
                    elif ttp20["type"] == "tool":
                        env.bundle_instance["objects"].append(ttp)
                    elif ttp20["type"] == "attack_pattern":
                        env.bundle_instance["objects"].append(ttp)
                    report_instance["object_refs"].append(ttp20["id"])
            else:
                report_instance["object_refs"].append(ttp.idref)


def convert_report(report, env):
    report_instance = create_basic_object("report", report, env)
    process_description_and_short_description(report_instance, report.header)
    new_env = env.newEnv(timestamp=report_instance["created"])
    if report.header:
        header_created_by_ref = process_information_source(report.header.information_source, report_instance, new_env)
        new_env.add_to_env(created_by_ref=header_created_by_ref)
        # process information source before any relationships
        add_string_property_to_description(report_instance, "intent", report.header.intents, True)
        if report.header.title is not None:
            report_instance["name"] = report.header.title
        convert_controlled_vocabs_to_open_vocabs(report_instance,
                                                 "labels" if get_option_value(
                                                     "spec_version") == "2.0" else "report_types",
                                                 report.header.intents, REPORT_LABELS_MAP, False)
    process_report_contents(report, new_env, report_instance)
    report_instance["published"] = report_instance["created"]
    info("The published property is required for STIX 2.0 Report %s, using the created property", 720, report_instance["id"])
    if report.related_reports is not None:
        # FIXME: related reports?
        info("Report Related_Reports in %s is not handled, yet.", 815, report_instance["id"])
    finish_basic_object(report.id_, report_instance, env, report.header)
    return report_instance


# threat actor

def add_motivations_to_threat_actor(sdo_instance, motivations):
    info("Using first Threat Actor motivation as primary_motivation. If more, as secondary_motivation", 719)

    if motivations[0].value is not None:
        sdo_instance["primary_motivation"] = map_vocabs_to_label(text_type(motivations[0].value), ATTACK_MOTIVATION_MAP)

    values = []

    if len(motivations) > 1:
        for m in motivations[1:]:
            if m.value is not None:
                values.append(m.value)

        if values:
            convert_controlled_vocabs_to_open_vocabs(sdo_instance, "secondary_motivations", values, ATTACK_MOTIVATION_MAP, False)


def convert_threat_actor(threat_actor, env):
    threat_actor_instance = create_basic_object("threat-actor", threat_actor, env)
    process_description_and_short_description(threat_actor_instance, threat_actor)
    new_env = env.newEnv(timestamp=threat_actor_instance["created"])
    new_env.add_to_env(created_by_ref=process_information_source(threat_actor.information_source, threat_actor_instance, new_env))
    # process information source before any relationships
    if threat_actor.identity is not None:
        if threat_actor.identity.id_:
            info("Threat Actor identity %s being used as basis of attributed-to relationship", 701, threat_actor.identity.id_)
        handle_relationship_to_objs([threat_actor.identity], threat_actor_instance["id"], new_env, "attributed-to")
    if threat_actor.title is not None:
        info("Threat Actor %s title is used for name property", 717, threat_actor.id_)
        threat_actor_instance["name"] = threat_actor.title
    elif threat_actor.identity.name:
        threat_actor_instance["name"] = threat_actor.identity.name
    elif isinstance(threat_actor.identity, CIQIdentity3_0Instance):
        convert_party_name(threat_actor.identity._specification.party_name, threat_actor_instance, False)
    convert_controlled_vocabs_to_open_vocabs(threat_actor_instance,
                                             "labels" if get_option_value(
                                                 "spec_version") == "2.0" else "threat_actor_types",
                                             threat_actor.types,
                                             THREAT_ACTOR_LABEL_MAP, False)
    add_multiple_statement_types_to_description(threat_actor_instance, threat_actor.intended_effects, "intended_effect")
    add_multiple_statement_types_to_description(threat_actor_instance, threat_actor.planning_and_operational_supports,
                                                "planning_and_operational_support")
    if get_option_value("spec_version") == "2.0":
        add_confidence_property_to_description(threat_actor_instance, threat_actor.confidence)
    else:  # 2.1
        add_confidence_to_object(threat_actor_instance, threat_actor.confidence)

    if threat_actor.motivations:
        add_motivations_to_threat_actor(threat_actor_instance, threat_actor.motivations)

    convert_controlled_vocabs_to_open_vocabs(threat_actor_instance, "sophistication", threat_actor.sophistications,
                                             THREAT_ACTOR_SOPHISTICATION_MAP, True)
    # handle relationships
    if threat_actor.observed_ttps is not None:
        handle_relationship_to_refs(threat_actor.observed_ttps, threat_actor_instance["id"], new_env, "uses")
    if threat_actor.associated_campaigns is not None:
        handle_relationship_from_refs(threat_actor.associated_campaigns, threat_actor_instance["id"], new_env, "attributed-to")
    if threat_actor.associated_actors:
        warn("All associated actors relationships of %s are assumed to not represent STIX 1.2 versioning", 710, threat_actor.id_)
        handle_relationship_to_refs(threat_actor.associated_actors, threat_actor_instance["id"], new_env, "related-to")

    finish_basic_object(threat_actor.id_, threat_actor_instance, env, threat_actor)
    return threat_actor_instance


# TTPs


def process_ttp_properties(sdo_instance, ttp, env, kill_chains_in_sdo=True):
    process_description_and_short_description(sdo_instance, ttp, True)
    add_multiple_statement_types_to_description(sdo_instance, ttp.intended_effects, "intended_effect")
    if hasattr(ttp, "title"):
        if "name" not in sdo_instance or sdo_instance["name"] is None:
            sdo_instance["name"] = ttp.title
        else:
            add_string_property_to_description(sdo_instance, "title", ttp.title, False)
    if ttp.exploit_targets is not None:
        handle_relationship_to_refs(ttp.exploit_targets, sdo_instance["id"], env,
                                    "targets", )
    # only populate kill chain phases if that is a property of the sdo_instance type, as indicated by kill_chains_in_sdo
    if kill_chains_in_sdo and hasattr(ttp, "kill_chain_phases"):
        convert_kill_chains(ttp.kill_chain_phases, sdo_instance)
    ttp_created_by_ref = process_information_source(ttp.information_source, sdo_instance,
                                                    env.newEnv(timestamp=sdo_instance["created"]))
    if ttp.related_ttps:
        warn("All associated indicators relationships of %s are assumed to not represent STIX 1.2 versioning", 710, ttp.id_)
        handle_relationship_to_refs(ttp.related_ttps, sdo_instance["id"], env.newEnv(timestamp=sdo_instance["created"]),
                                    "related-to", ttp_created_by_ref)
    if hasattr(ttp, "related_packages") and ttp.related_packages is not None:
        for p in ttp.related_packages:
            warn("Related_Packages type in %s not supported in STIX 2.0", 402, ttp.id_)


def convert_attack_pattern(ap, ttp, env, ttp_id_used):
    attack_Pattern_instance = create_basic_object("attack-pattern", ap, env, ttp.id_, not ttp_id_used)
    if ap.title is not None:
        attack_Pattern_instance["name"] = ap.title
    process_description_and_short_description(attack_Pattern_instance, ap)
    if ap.capec_id is not None:
        attack_Pattern_instance["external_references"] = [{"source_name": "capec", "external_id": ap.capec_id}]
    process_ttp_properties(attack_Pattern_instance, ttp, env)
    finish_basic_object(ttp.id_, attack_Pattern_instance, env, ap)
    return attack_Pattern_instance


def convert_malware_instance(mal, ttp, env, ttp_id_used):
    malware_instance_instance = create_basic_object("malware", mal, env, ttp.id_, not ttp_id_used)
    # TODO: names?
    if mal.title is not None:
        malware_instance_instance["name"] = mal.title
    process_description_and_short_description(malware_instance_instance, mal)
    convert_controlled_vocabs_to_open_vocabs(malware_instance_instance,
                                             "labels" if get_option_value("spec_version") == "2.0" else "malware_types",
                                             mal.types,
                                             MALWARE_LABELS_MAP,
                                             False)
    if mal.names is not None:
        for n in mal.names:
            if "name" not in malware_instance_instance:
                malware_instance_instance["name"] = text_type(n)
            else:
                # TODO: add to description?
                warn("Only one name for malware is allowed for %s in STIX 2.0 - used first one", 508, malware_instance_instance["id"])
    if isinstance(mal, MAECInstance):
        warn("MAEC content in %s cannot be represented in STIX 2.0", 426, ttp.id_)
    process_ttp_properties(malware_instance_instance, ttp, env)
    finish_basic_object(ttp.id_, malware_instance_instance, env, mal)
    return malware_instance_instance


def convert_behavior(behavior, ttp, env):
    resources_generated = []
    first_one = True
    if behavior.attack_patterns is not None:
        for ap in behavior.attack_patterns:
            new_obj = convert_attack_pattern(ap, ttp, env, first_one)
            env.bundle_instance["objects"].append(new_obj)
            resources_generated.append(new_obj)
            first_one = False
    if behavior.malware_instances is not None:
        for mal in behavior.malware_instances:
            new_obj = convert_malware_instance(mal, ttp, env, first_one)
            env.bundle_instance["objects"].append(new_obj)
            resources_generated.append(new_obj)
            first_one = False
    if behavior.exploits is not None:
        for e in behavior.exploits:
            warn("TTP/Behavior/Exploits/Exploit in %s not supported in STIX 2.0", 408, ttp.id_)
    return resources_generated


def convert_tool(tool, ttp, env, first_one):
    tool_instance = create_basic_object("tool", tool, env, ttp.id_, not first_one)
    if tool.name is not None:
        tool_instance["name"] = tool.name
    process_description_and_short_description(tool_instance, tool)
    add_string_property_to_description(tool_instance, "vendor", tool.vendor)
    add_string_property_to_description(tool_instance, "service_pack", tool.service_pack)
    # TODO: add tool_specific_data to descriptor <-- Not Implemented!

    if tool.tool_hashes is not None:
        # FIXME: add tool_hashes to descriptor
        info("Tool Tool_Hashes in %s is not handled, yet.", 815, tool_instance["id"])

    # TODO: add tool_configuration to descriptor <-- Not Implemented!
    # TODO: add execution_environment to descriptor <-- Not Implemented!
    # TODO: add errors to descriptor <-- Not Implemented!
    # TODO: add compensation_model to descriptor <-- Not Implemented!
    add_string_property_to_description(tool_instance, "title", tool.title)
    convert_controlled_vocabs_to_open_vocabs(tool_instance,
                                             "labels" if get_option_value("spec_version") == "2.0" else "tool_types",
                                             tool.type_,
                                             TOOL_LABELS_MAP,
                                             False)
    tool_instance["tool_version"] = tool.version
    process_ttp_properties(tool_instance, ttp, env)
    finish_basic_object(ttp.id_, tool_instance, env, tool)
    return tool_instance


def convert_infrastructure(infra, ttp, env, first_one):
    infrastructure_instance = create_basic_object("infrastructure", infra, env, not first_one)
    if infra.title is not None:
        infrastructure_instance["name"] = infra.title
    process_description_and_short_description(infrastructure_instance, infra)
    convert_controlled_vocabs_to_open_vocabs(infrastructure_instance, "labels", infra.types, {}, False)
    info("No 'first_seen' data on %s - using timestamp", 904, infra.id_ if infra.id_ else ttp.id_)
    infrastructure_instance["first_seen"] = convert_timestamp_of_stix_object(infra, infrastructure_instance["created"])

    if infra.observable_characterization is not None:
        # FIXME: add observable_characterizations
        info("Infrastructure Observable_Characterization in %s is not handled, yet.", 815, infrastructure_instance["id"])
    process_ttp_properties(infrastructure_instance, ttp, env)
    finish_basic_object(ttp.id_, infrastructure_instance, env, infra)
    return infrastructure_instance


def convert_resources(resources, ttp, env, generated_ttps):
    resources_generated = []
    first_one = (generated_ttps == [])
    if resources.tools is not None:
        for t in resources.tools:
            new_obj = convert_tool(t, ttp, env, first_one)
            env.bundle_instance["objects"].append(new_obj)
            resources_generated.append(new_obj)
            first_one = False
    if resources.infrastructure is not None:
        if get_option_value("infrastructure"):
            new_obj = convert_infrastructure(resources.infrastructure, ttp, env)
            env.bundle_instance["objects"].append(new_obj)
            resources_generated.append(new_obj)
        else:
            warn("Infrastructure in %s not part of STIX 2.0", 409, ttp.id_ or "")
    return resources_generated


def convert_identity_for_victim_target(identity, ttp, env, ttp_generated):
    identity_instance = convert_identity(identity, env, parent_id=ttp.id_ if not ttp_generated else None)
    env.bundle_instance["objects"].append(identity_instance)
    process_ttp_properties(identity_instance, ttp, env, False)
    finish_basic_object(ttp.id_, identity_instance, identity, env, identity_instance["id"])
    return identity_instance


def convert_victim_targeting(victim_targeting, ttp, env, ttp_generated):
    if victim_targeting.targeted_systems:
        for v in victim_targeting.targeted_systems:
            warn("Targeted systems on %s are not a victim target in STIX 2.0", 410, ttp.id_)
    if victim_targeting.targeted_information:
        for v in victim_targeting.targeted_information:
            warn("Targeted information on %s is not a victim target in STIX 2.0", 411, ttp.id_)
    if hasattr(victim_targeting, "technical_details") and victim_targeting.targeted_technical_details is not None:
        for v in victim_targeting.targeted_technical_details:
            warn("Targeted technical details on %s are not a victim target in STIX 2.0", 412, ttp.id_)
    if victim_targeting.identity:
        identity_instance = convert_identity_for_victim_target(victim_targeting.identity, ttp, env, ttp_generated)
        if identity_instance:
            warn("%s generated an identity associated with a victim", 713, ttp.id_)
            if ttp_generated:
                env.bundle_instance["relationships"].append(
                    create_relationship(ttp.id_, identity_instance["id"], env, "targets"))
                # the relationship has been created, so its not necessary to propagate it up
                return None
            else:
                return identity_instance
    # nothing generated
    return None


def convert_ttp(ttp, env):
    if hasattr(ttp, "timestamp") and ttp.timestamp:
        new_env = env.newEnv(timestamp=ttp.timestamp)
    else:
        new_env = env
    generated_objs = []
    if ttp.behavior is not None:
        generated_objs.extend(convert_behavior(ttp.behavior, ttp, new_env))
    if ttp.resources is not None:
        generated_objs.extend(convert_resources(ttp.resources, ttp, env, generated_objs))
    if hasattr(ttp, "kill_chain_phases") and ttp.kill_chain_phases is not None:
        for phase in ttp.kill_chain_phases:
            warn("Kill Chains type in %s not supported in STIX 2.0", 413, ttp.id_)
    if ttp.victim_targeting is not None:
        victim_target = convert_victim_targeting(ttp.victim_targeting, ttp, new_env, generated_objs)
        if not victim_target:
            warn("Victim Target in %s did not generate any STIX 2.0 object", 414, ttp.id_)
        else:
            return generated_objs.append(victim_target)
    # victims weren't involved, check existing list
    if not generated_objs and ttp.id_ is not None:
        warn("TTP %s did not generate any STIX 2.0 object", 415, ttp.id_)
    return generated_objs


# package


def handle_embedded_object(obj, env):
    new20 = None
    new20s = None
    # campaigns
    if isinstance(obj, Campaign):
        new20 = convert_campaign(obj, env)
        env.bundle_instance["objects"].append(new20)
    # coas
    elif isinstance(obj, CourseOfAction):
        new20 = convert_course_of_action(obj, env)
        env.bundle_instance["objects"].append(new20)
    # exploit-targets
    elif isinstance(obj, ExploitTarget):
        new20s = convert_exploit_target(obj, env)
    # identities
    elif isinstance(obj, Identity) or isinstance(obj, CIQIdentity3_0Instance):
        new20 = convert_identity(obj, env)
        env.bundle_instance["objects"].append(new20)
    # incidents
    elif get_option_value("incidents") and isinstance(obj, Incident):
        new20 = convert_incident(obj, env)
        env.bundle_instance["objects"].append(new20)
    # indicators
    elif isinstance(obj, Indicator):
        new20 = convert_indicator(obj, env)
        env.bundle_instance["indicators"].append(new20)
    # observables
    elif isinstance(obj, Observable):
        new20 = convert_observed_data(obj, env)
        env.bundle_instance["observed_data"].append(new20)
    # reports
    elif stix.__version__ >= "1.2.0.0" and isinstance(obj, Report):
        new20 = convert_report(obj, env)
        env.bundle_instance["reports"].append(new20)
    # threat actors
    elif isinstance(obj, ThreatActor):
        new20 = convert_threat_actor(obj, env)
        env.bundle_instance["objects"].append(new20)
    # ttps
    elif isinstance(obj, TTP):
        new20s = convert_ttp(obj, env)
    if new20:
        return [new20]
    elif new20s:
        return new20s
    else:
        warn("No STIX 2.0 object generated from embedded object %s", 416, identifying_info(obj))
        return []


def initialize_bundle_lists(bundle_instance):
    bundle_instance["relationships"] = []
    bundle_instance["indicators"] = []
    bundle_instance["reports"] = []
    bundle_instance["observed_data"] = []
    bundle_instance["objects"] = []


def finalize_bundle(bundle_instance):
    if _KILL_CHAINS_PHASES != {}:
        for ind20 in bundle_instance["indicators"]:
            if "kill_chain_phases" in ind20:
                fixed_kill_chain_phases = []
                for kcp in ind20["kill_chain_phases"]:
                    if isinstance(kcp, str):
                        # noinspection PyBroadException
                        try:
                            kill_chain_phase_in_20 = _KILL_CHAINS_PHASES[kcp]
                            fixed_kill_chain_phases.append(kill_chain_phase_in_20)
                        except KeyError:
                            error("Dangling kill chain phase id in indicator %s", 607, ind20["id"])
                    else:
                        fixed_kill_chain_phases.append(kcp)
                ind20["kill_chain_phases"] = fixed_kill_chain_phases
    # ttps

    fix_relationships(bundle_instance["relationships"], bundle_instance)

    fix_cybox_relationships(bundle_instance["observed_data"])
    # need to remove observed-data not used at the top level

    if stix.__version__ >= "1.2.0.0":
        add_relationships_to_reports(bundle_instance)

    # source and target_ref are taken care in fix_relationships(...)
    _TO_MAP = ("id", "idref", "created_by_ref", "external_references",
               "marking_ref", "object_marking_refs", "object_refs",
               "sighting_of_ref", "observed_data_refs", "where_sighted_refs")

    _LOOK_UP = ("", u"", [], None, dict())

    to_remove = []

    if "indicators" in bundle_instance:
        interatively_resolve_placeholder_refs()
        for ind in bundle_instance["indicators"]:
            if "pattern" in ind:
                final_pattern = fix_pattern(ind["pattern"])
                if final_pattern:
                    if final_pattern.contains_placeholder():
                        warn("At least one PLACEHOLDER idref was not resolved in %s", 205, ind["id"])
                    if final_pattern.contains_unconverted_term():
                        warn("At least one observable could not be converted in %s", 206, ind["id"])
                    if (isinstance(final_pattern, ComparisonExpressionForElevator) or
                            isinstance(final_pattern, UnconvertedTerm)):
                        ind["pattern"] = "[%s]" % final_pattern
                    elif isinstance(final_pattern, ParentheticalExpressionForElevator):
                        result = final_pattern.expression.partition_according_to_object_path()
                        if isinstance(result, CompoundObservationExpressionForElevator):
                            ind["pattern"] = "%s" % result
                        else:
                            ind["pattern"] = "[%s]" % result
                    else:
                        ind["pattern"] = text_type(final_pattern.partition_according_to_object_path())

    bundle_instance["objects"].extend(bundle_instance["indicators"])
    bundle_instance["indicators"] = []
    bundle_instance["objects"].extend(bundle_instance["relationships"])
    bundle_instance["relationships"] = []
    bundle_instance["objects"].extend(bundle_instance["observed_data"])
    bundle_instance["observed_data"] = []
    bundle_instance["objects"].extend(bundle_instance["reports"])
    bundle_instance["reports"] = []

    for entry in iterpath(bundle_instance):
        path, value = entry
        last_field = path[-1]
        iter_field = path[-2] if len(path) >= 2 else ""

        if value in _LOOK_UP:
            to_remove.append(list(path))

        if isinstance(value, (list, dict)):
            continue

        if last_field in _TO_MAP or iter_field in _TO_MAP:
            if reference_needs_fixing(value) and exists_id_key(value):
                stix20_id = get_id_value(value)

                if stix20_id[0] is None:
                    warn("1.X ID: %s was not mapped to STIX 2.0 ID", 603, value)
                    continue

                operation_on_path(bundle_instance, path, stix20_id[0])
                info("Found STIX 1.X ID: %s replaced by %s", 702, value, stix20_id[0])
            elif reference_needs_fixing(value) and not exists_id_key(value):
                warn("1.X ID: %s was not mapped to STIX 2.0 ID", 603, value)

    for item in to_remove:
        operation_on_path(bundle_instance, item, "", op=2)

    if "objects" in bundle_instance:
        remove_pattern_objects(bundle_instance)
    else:
        error("EMPTY BUNDLE -- No objects created from 1.x input document!", 208)


def get_identity_from_package(information_source, env):
    if information_source:
        if information_source.identity is not None:
            return get_identity_ref(information_source.identity, env, from_package=True)
        if information_source.contributing_sources is not None:
            if information_source.contributing_sources.source is not None:
                sources = information_source.contributing_sources.source

                if len(sources) > 1:
                    warn("Only one identity allowed - using first one.", 510)

                for source in sources:
                    if source.identity is not None:
                        return get_identity_ref(source.identity, env, from_package=True)
    return None


def convert_package(stix_package, env):
    bundle_instance = {"type": "bundle"}
    bundle_instance["id"] = generate_stix20_id("bundle", stix_package.id_)
    env.bundle_instance = bundle_instance
    initialize_bundle_lists(bundle_instance)

    if get_option_value("spec_version") == "2.0":
        bundle_instance["spec_version"] = "2.0"

    if hasattr(stix_package, "timestamp"):
        env.timestamp = stix_package.timestamp

    # created_by_idref from the command line is used instead of the one from the package, if given
    if not env.created_by_ref and hasattr(stix_package.stix_header, "information_source"):
        env.created_by_ref = get_identity_from_package(stix_package.stix_header.information_source, env)

    # Markings are processed in the beginning for handling later for each SDO.
    for marking_specification in navigator.iterwalk(stix_package):
        if isinstance(marking_specification, MarkingSpecification):
            bundle_instance["objects"].extend(convert_marking_specification(marking_specification, env))

    # do observables first, especially before indicators!

    # kill chains
    if stix_package.ttps and stix_package.ttps.kill_chains:
        for kc in stix_package.ttps.kill_chains:
            process_kill_chain(kc)

    # observables
    if stix_package.observables is not None:
        for o_d in stix_package.observables:
            o_d20 = convert_observed_data(o_d, env)
            bundle_instance["observed_data"].append(o_d20)

    # campaigns
    if stix_package.campaigns:
        for camp in stix_package.campaigns:
            camp20 = convert_campaign(camp, env)
            bundle_instance["objects"].append(camp20)

    # coas
    if stix_package.courses_of_action:
        for coa in stix_package.courses_of_action:
            coa20 = convert_course_of_action(coa, env)
            bundle_instance["objects"].append(coa20)

    # exploit-targets
    if stix_package.exploit_targets:
        for et in stix_package.exploit_targets:
            convert_exploit_target(et, env)

    # incidents
    if get_option_value("incidents"):
        if stix_package.incidents:
            for i in stix_package.incidents:
                i20 = convert_incident(i, env)
                bundle_instance["objects"].append(i20)

    # indicators
    if stix_package.indicators:
        for i in stix_package.indicators:
            i20 = convert_indicator(i, env)
            bundle_instance["indicators"].append(i20)

    # reports
    if stix.__version__ >= "1.2.0.0" and stix_package.reports:
        for report in stix_package.reports:
            report20 = convert_report(report, env)
            bundle_instance["reports"].append(report20)

    # threat actors
    if stix_package.threat_actors:
        for ta in stix_package.threat_actors:
            ta20 = convert_threat_actor(ta, env)
            bundle_instance["objects"].append(ta20)

    # ttps
    if stix_package.ttps:
        for ttp in stix_package.ttps:
            convert_ttp(ttp, env)

    finalize_bundle(bundle_instance)
    return bundle_instance
