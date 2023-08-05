#include "input.h"
#include "src/helpers.h"
#include "storm-parsers/api/storm-parsers.h"
#include "storm/storage/jani/Property.h"

void define_property(py::module& m) {
    py::class_<storm::jani::Property>(m, "Property", "Property")
        .def(py::init<std::string const&, std::shared_ptr<storm::logic::Formula const> const&, std::set<storm::expressions::Variable> const&, std::string const&>(), "Construct property from formula", py::arg("name"), py::arg("formula"), py::arg("undefined_constants") = std::set<storm::expressions::Variable>(), py::arg("comment") = "")
        .def(py::init<storm::jani::Property>())
        .def_property_readonly("name", &storm::jani::Property::getName, "Obtain the name of the property")
        .def_property_readonly("raw_formula", &storm::jani::Property::getRawFormula, "Obtain the formula directly")
        .def("__str__", &streamToString<storm::jani::Property>)
    ;
}


// Define python bindings
void define_input(py::module& m) {

    // Parse Prism program
    m.def("parse_prism_program", &storm::api::parseProgram, "Parse Prism program", py::arg("path"), py::arg("prism_compat") = false, py::arg("simplify") = true);
    // Parse Jani model
    m.def("parse_jani_model", [](std::string const& path){
            return storm::api::parseJaniModel(path);
        }, "Parse Jani model", py::arg("path"));

    // JaniType
    py::enum_<storm::jani::ModelType>(m, "JaniModelType", "Type of the Jani model")
        .value("DTMC", storm::jani::ModelType::DTMC)
        .value("CTMC", storm::jani::ModelType::CTMC)
        .value("MDP", storm::jani::ModelType::MDP)
        .value("CTMDP", storm::jani::ModelType::CTMDP)
        .value("MA", storm::jani::ModelType::MA)
        .value("LTS", storm::jani::ModelType::LTS)
        .value("TA", storm::jani::ModelType::TA)
        .value("PTA", storm::jani::ModelType::PTA)
        .value("STA", storm::jani::ModelType::STA)
        .value("HA", storm::jani::ModelType::HA)
        .value("PHA", storm::jani::ModelType::PHA)
        .value("SHA", storm::jani::ModelType::SHA)
        .value("UNDEFINED", storm::jani::ModelType::UNDEFINED)
    ;

    // SymbolicModelDescription
    py::class_<storm::storage::SymbolicModelDescription>(m, "SymbolicModelDescription", "Symbolic description of model")
        .def(py::init<storm::prism::Program const&>(), "Construct from Prism program", py::arg("prism_program"))
        .def(py::init<storm::jani::Model const&>(), "Construct from Jani model", py::arg("jani_model"))
        .def_property_readonly("is_prism_program", &storm::storage::SymbolicModelDescription::isPrismProgram, "Flag if program is in Prism format")
        .def_property_readonly("is_jani_model", &storm::storage::SymbolicModelDescription::isJaniModel, "Flag if program is in Jani format")
        .def("parse_constant_definitions", &storm::storage::SymbolicModelDescription::parseConstantDefinitions, "Parse given constant definitions", py::arg("String containing constants and their values"))
        .def("instantiate_constants", [](storm::storage::SymbolicModelDescription const& description, std::map<storm::expressions::Variable, storm::expressions::Expression> const& constantDefinitions) {
                return description.preprocess(constantDefinitions);
            }, "Instantiate constants in symbolic model description", py::arg("constant_definitions"))
        .def("as_jani_model", [](storm::storage::SymbolicModelDescription& description) {
                return description.asJaniModel();
            }, "Return Jani model")
        .def("as_prism_program", [](storm::storage::SymbolicModelDescription& description) {
                return description.asPrismProgram();
            }, "Return Prism program")
    ;

    // PrismProgram and JaniModel can be converted into SymbolicModelDescription
    py::implicitly_convertible<storm::prism::Program, storm::storage::SymbolicModelDescription>();
    py::implicitly_convertible<storm::jani::Model, storm::storage::SymbolicModelDescription>();
}
