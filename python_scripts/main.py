from conversor import ConversorSADT
from conversor import ConversorConsulta
from conversor import ConversorHonorario


# conversor_consulta = ConversorConsulta("xml_files\Consultas\lote_sulamerica_1.xml")
# conversor_consulta.salvar_excel()


# conversor_sadt = ConversorSADT("xml_files\SADT\lote_bacen_1.xml")
# conversor_sadt.salvar_excel()

conversor_honorario = ConversorHonorario("xml_files\Honorario_individual\lote_58.xml")
conversor_honorario.salvar_excel()

