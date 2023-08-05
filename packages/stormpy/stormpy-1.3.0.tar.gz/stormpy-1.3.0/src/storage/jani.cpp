#include "jani.h"
#include <storm/storage/jani/Model.h>
#include <storm/storage/jani/JSONExporter.h>
#include <storm/storage/expressions/ExpressionManager.h>
#include <storm/logic/RewardAccumulationEliminationVisitor.h>
#include "src/helpers.h"

using namespace storm::jani;

std::string janiToString(Model const& m) {
    std::stringstream str;
    JsonExporter::toStream(m, {}, str);
    return str.str();
}

void define_jani(py::module& m) {

    py::class_<Model, std::shared_ptr<Model>> md(m, "JaniModel", "A Jani Model");
    md.def(py::init<Model>(), "other_model"_a)
        .def_property_readonly("name", &Model::getName, "model name")
        .def_property_readonly("model_type", &storm::jani::Model::getModelType, "Model type")
        .def("set_model_type", &Model::setModelType, "Sets (only) the model type")
        .def_property_readonly("automata", [](const Model& model) -> auto& {return model.getAutomata();}, "get automata")
        .def_property_readonly("global_variables", [](const Model& model) -> auto& {return model.getGlobalVariables();})
        .def_property_readonly("constants", [](const Model& model) -> auto& {return model.getConstants();}, "get constants")
        .def("get_constant", &Model::getConstant, "name"_a, "get constant by name")
        .def("restrict_edges", &Model::restrictEdges, "restrict model to edges given by set", py::arg("edge_set"))
        .def_property_readonly("expression_manager", &Model::getExpressionManager, "get expression manager", pybind11::return_value_policy::reference_internal)
        .def_property_readonly("has_undefined_constants", &Model::hasUndefinedConstants, "Flag if program has undefined constants")
        .def_property_readonly("undefined_constants_are_graph_preserving", &Model::undefinedConstantsAreGraphPreserving, "Flag if the undefined constants do not change the graph structure")
        .def("__str__", &janiToString)
        .def_property("initial_states_restriction", &Model::getInitialStatesRestriction, &Model::setInitialStatesRestriction, "initial states restriction")
        .def("define_constants", &Model::defineUndefinedConstants, "define constants with a mapping from the corresponding expression variables to expressions", py::arg("map"))
        .def("substitute_constants", &Model::substituteConstants, "substitute constants")
        .def("remove_constant", &Model::removeConstant, "remove a constant. Make sure the constant does not appear in the model.", "constant_name"_a)
        .def("get_automaton_index", &Model::getAutomatonIndex, "name"_a, "get index for automaton name")
        .def("add_automaton", &Model::addAutomaton, "automaton"_a, "add an automaton (with a unique name)")
        .def("set_standard_system_composition", &Model::setStandardSystemComposition, "sets the composition to the standard composition")
        .def("replace_automaton", &Model::replaceAutomaton, "index"_a, "new_automaton"_a, "replace automaton at index")
        .def("check_valid", &Model::checkValid, "Some basic checks to ensure validity")
        .def("substitute_functions", [](Model& model) {model.substituteFunctions();}, "substitute functions")
        .def_static("encode_automaton_and_edge_index", &Model::encodeAutomatonAndEdgeIndices, "get edge/automaton-index")
        .def_static("decode_automaton_and_edge_index", &Model::decodeAutomatonAndEdgeIndices, "get edge and automaton from edge/automaton index")
        .def("make_standard_compliant", &Model::makeStandardJaniCompliant, "make standard JANI compliant")
        .def("has_standard_composition", &Model::hasStandardComposition, "is the composition the standard composition")
        .def("finalize", &Model::finalize,"finalizes the model. After this action, be careful changing the data structure.")
        .def("to_dot", [](Model& model) {std::stringstream ss; model.writeDotToStream(ss); return ss.str(); })
    ;

    py::class_<Automaton, std::shared_ptr<Automaton>> automaton(m, "JaniAutomaton", "A Jani Automation");
    automaton.def(py::init<std::string, storm::expressions::Variable>())
        .def_property_readonly("edges",[](const Automaton& a) -> auto& {
            return a.getEdges();
        }, "get edges")
        .def_property_readonly("name", &Automaton::getName)
        .def_property_readonly("location_variable", &Automaton::getLocationExpressionVariable)
        .def_property_readonly("variables", [](Automaton& aut) -> VariableSet& {return aut.getVariables();}, py::return_value_policy::reference_internal)
        .def_property_readonly("locations", [](Automaton& aut) -> auto& {return aut.getLocations();})
        .def("add_location", &Automaton::addLocation, "location"_a, "adds a new location, returns the index")
        .def("add_initial_location", [](Automaton& aut, uint64_t index) { aut.addInitialLocation(index); }, "index"_a)
        .def_property_readonly("initial_location_indices", &Automaton::getInitialLocationIndices)
        .def_property("initial_states_restriction", [](Automaton& aut) { aut.getInitialStatesExpression(); }, &Automaton::setInitialStatesRestriction, "initial state restriction")
        .def("add_edge", &Automaton::addEdge, "edge"_a)

    ;

    py::class_<Edge, std::shared_ptr<Edge>> edge(m, "JaniEdge", "A Jani Edge");
    edge.def(py::init<uint64_t, uint64_t, boost::optional<storm::expressions::Expression>, std::shared_ptr<TemplateEdge>, std::vector<std::pair<uint64_t, storm::expressions::Expression>>>(),
            "source_location_index"_a, "action_index"_a, "rate"_a, "template_edge"_a, "destinations_with_probabilities"_a)
        .def_property_readonly("source_location_index", &Edge::getSourceLocationIndex, "index for source location")
        .def_property_readonly("destinations", [](Edge const& e) -> auto&  {
                return e.getDestinations();
             }, "edge destinations")
        .def_property_readonly("action_index", &Edge::getActionIndex, "action index")
        .def_property_readonly("template_edge", &Edge::getTemplateEdge, "template edge")
        .def_property_readonly("rate", &Edge::getOptionalRate, "edge rate")
        .def_property_readonly("nr_destinations", &Edge::getNumberOfDestinations, "nr edge destinations")
        .def_property_readonly("guard", &Edge::getGuard, "edge guard")
        .def_property("color", &Edge::getColor, &Edge::setColor, "color for the edge")
        .def("substitute", &Edge::substitute, py::arg("mapping"))
        .def("has_silent_action", &Edge::hasSilentAction, "Is the edge labelled with the silent action")
    ;

    py::class_<TemplateEdge, std::shared_ptr<TemplateEdge>> templateEdge(m, "JaniTemplateEdge", "Template edge, internal data structure for edges");
    templateEdge.def(py::init<storm::expressions::Expression>())
            .def_property_readonly("assignments", [](TemplateEdge& te) -> auto& { return te.getAssignments(); })
            .def_property("guard", &TemplateEdge::getGuard, &TemplateEdge::setGuard)
            .def_property_readonly("destinations",[](TemplateEdge& te) -> auto& { return te.getDestinations(); })
            .def("add_destination", &TemplateEdge::addDestination)
            ;

    py::class_<EdgeDestination, std::shared_ptr<EdgeDestination>> edgeDestination(m, "JaniEdgeDestination", "Destination in Jani");
    edgeDestination.def_property_readonly("target_location_index", &EdgeDestination::getLocationIndex)
        .def_property_readonly("probability", &EdgeDestination::getProbability)
        .def_property_readonly("assignments", &EdgeDestination::getOrderedAssignments)
    ;

    py::class_<TemplateEdgeDestination, std::shared_ptr<TemplateEdgeDestination>> templateEdgeDestination(m, "JaniTemplateEdgeDestination", "Template edge destination, internal data structure for edge destinations");
    templateEdgeDestination.def(py::init<OrderedAssignments>(), "ordered_assignments"_a)
            .def_property_readonly("assignments", [](TemplateEdgeDestination& ted) -> auto& {return ted.getOrderedAssignments();});

    py::class_<OrderedAssignments, std::shared_ptr<OrderedAssignments>> orderedAssignments(m, "JaniOrderedAssignments", "Set of assignments");
    orderedAssignments.def("__iter__", [](OrderedAssignments &v) {
                return py::make_iterator(v.begin(), v.end());
            }, py::keep_alive<0, 1>()) /* Keep vector alive while iterator is used */
        .def("__str__", &streamToString<OrderedAssignments>)
        .def("clone", &OrderedAssignments::clone, "clone assignments (performs a deep copy)")
        .def("substitute", &OrderedAssignments::substitute, "substitute in rhs according to given substitution map", "substitution_map"_a)
        .def("add", [](OrderedAssignments& oa, Assignment const& newAssignment, bool addToExisting) {return oa.add(newAssignment, addToExisting); }, "new_assignment"_a, "add_to_existing"_a = false)
    ;

    py::class_<Assignment, std::shared_ptr<Assignment>> assignment(m, "JaniAssignment", "Jani Assignment");
    assignment.def(py::init<Variable const&,storm::expressions::Expression const&,int64_t>(), "lhs"_a, "rhs"_a, "lvl"_a = 0)
        .def("__str__", &streamToString<Assignment>)
        .def_property("expression", &Assignment::getAssignedExpression, &Assignment::setAssignedExpression)
    ;

    py::class_<Location, std::shared_ptr<Location>> location(m, "JaniLocation", "A Location in JANI");
    location.def_property_readonly("name", &Location::getName, "name of the location")
            .def_property_readonly("assignments", [](Location& loc) {loc.getAssignments();}, "location assignments")
            ;

    py::class_<VariableSet, std::shared_ptr<VariableSet>> variableSet(m, "JaniVariableSet", "Jani Set of Variables");
    variableSet.def(py::init<>())
        .def("__iter__", [](VariableSet &v) {
            return py::make_iterator(v.begin(), v.end());
        }, py::keep_alive<0, 1>())
        .def("add_variable", [](VariableSet& vs, Variable& v) -> void { vs.addVariable(v); })
        .def("add_bounded_integer_variable", [](VariableSet& vs, BoundedIntegerVariable& v) -> auto& { return vs.addVariable(v); /*return vs.getVariable(v.getExpressionVariable());*/ }, py::return_value_policy::reference_internal, "variable"_a)
        .def("empty", &VariableSet::empty, "is there a variable in the set?")
        .def("get_variable_by_name", [](VariableSet& v, std::string const& name) -> auto& { return v.getVariable(name);})
        .def("get_variable_by_expr_variable", [](VariableSet& v, storm::expressions::Variable const& var) -> auto& { return v.getVariable(var);})
    ;

    py::class_<Variable, std::shared_ptr<Variable>> variable(m, "JaniVariable", "A Variable in JANI");
    variable.def_property_readonly("name", &Variable::getName, "name of constant")
            .def_property_readonly("expression_variable", &Variable::getExpressionVariable, "expression variable for this variable")
            ;

    py::class_<BoundedIntegerVariable, std::shared_ptr<BoundedIntegerVariable>> bivariable(m, "JaniBoundedIntegerVariable", "A Bounded Integer", variable);
    bivariable.def(py::init<std::string, storm::expressions::Variable, storm::expressions::Expression, storm::expressions::Expression, storm::expressions::Expression>(),
                "name"_a, "expression_variable"_a, "init_value"_a, "lower_bound"_a, "upper_bound"_a)
            .def(py::init<std::string, storm::expressions::Variable, storm::expressions::Expression, storm::expressions::Expression>(),
                 "name"_a, "expression_variable"_a, "lower_bound"_a, "upper_bound"_a);;

    py::class_<Constant, std::shared_ptr<Constant>> constant(m, "JaniConstant", "A Constant in JANI");
    constant.def_property_readonly("defined", &Constant::isDefined, "is constant defined by some expression")
        .def_property_readonly("name", &Constant::getName, "name of constant")
        .def_property_readonly("type", &Constant::getType, "type of constant")
        .def_property_readonly("expression_variable", &Constant::getExpressionVariable, "expression variable for this constant")
    ;


    m.def("eliminate_reward_accumulations", [](const Model& model, std::vector<Property>& properties) {
            storm::logic::RewardAccumulationEliminationVisitor v(model);
            v.eliminateRewardAccumulations(properties);
            return properties;
        }, "Eliminate reward accumulations", py::arg("model"), py::arg("properties"));



}