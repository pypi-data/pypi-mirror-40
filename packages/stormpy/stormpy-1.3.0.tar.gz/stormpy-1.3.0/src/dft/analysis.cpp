#include "analysis.h"

#include "storm-dft/parser/DFTJsonParser.h"
#include "storm-dft/builder/ExplicitDFTModelBuilder.h"
#include "storm-dft/storage/dft/DFTIsomorphism.h"


// Thin wrapper for DFT analysis
template<typename ValueType>
std::vector<ValueType> analyzeDFT(storm::storage::DFT<ValueType> const& dft, std::vector<std::shared_ptr<storm::logic::Formula const>> const& properties, bool symred, bool allowModularisation, bool enableDC) {
    typename storm::modelchecker::DFTModelChecker<ValueType>::dft_results dftResults = storm::api::analyzeDFT(dft, properties, symred, allowModularisation, enableDC, false);
    std::vector<ValueType> results;
    for (auto result : dftResults) {
        results.push_back(boost::get<ValueType>(result));
    }
    return results;
}


// Define python bindings
void define_analysis(py::module& m) {

    m.def("analyze_dft", &analyzeDFT<double>, "Analyze the DFT", py::arg("dft"), py::arg("properties"), py::arg("symred")=true, py::arg("allow_modularisation")=false, py::arg("enable_dont_care")=true);

}
