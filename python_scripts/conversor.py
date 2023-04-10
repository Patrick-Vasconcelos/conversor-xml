import xml.etree.ElementTree as et
import pandas as pd



class ConversorXml():
    def __init__(self, path:str, lote: dict = {'ans': "http://www.ans.gov.br/padroes/tiss/schemas"}) -> None:
        self.path = path
        self.root = et.parse(self.path)
        self.lote = lote
        self.etree = et.parse(self.path)
        self.eroot = self.etree.getroot()

    def cria_dicionario(self,itens, path):
        dicionario = {}
        for item in itens.findall(path, self.lote):
            dicionario[f"{item.tag.removeprefix('{http://www.ans.gov.br/padroes/tiss/schemas}')}"] = f"{item.text}"
        return dicionario

    def carregar_identificacao_transacao(self,item):
        dict_identificacao_transacao = self.cria_dicionario(itens=item,path='ans:identificacaoTransacao//')
        return dict_identificacao_transacao
    
    def carregar_origem(self,item):
        dict_origem = self.cria_dicionario(itens=item, path = './/ans:identificacaoPrestador//')
        return dict_origem

    def carregar_destino(self,item):
        dict_destino = self.cria_dicionario(itens=item, path='.//ans:registroANS')
        return dict_destino
    
    def carregar_padrao(self,item):
        dict_padrao = self.cria_dicionario(itens=item, path='ans:Padrao')
        return dict_padrao

    def carregar_cabecalho(self):
        cabecalho = self.eroot.findall('.//ans:cabecalho', self.lote)
        for item in cabecalho:
            dicionario = {}
            identificacao_transacao = self.carregar_identificacao_transacao(item=item)
            dicionario.update(identificacao_transacao)
            origem = self.carregar_origem(item=item)
            dicionario.update(origem)
            destino = self.carregar_destino(item=item)
            dicionario.update(destino)
            padrao = self.carregar_padrao(item=item)
            dicionario.update(padrao)
            
           
        return dicionario

    def salvar_excel(self):
        
        guias = self.carregar_guias()

        df = pd.DataFrame(guias, columns=['registroANS', 'numeroGuiaPrestador', 'numeroGuiaOperadora', 'numeroCarteira', 'atendimentoRN',
                                            'nomeBeneficiario', 'codigoPrestadorNaOperadora', 'nomeContratado', 'CNES', 
                                            'nomeProfissional' , 'conselhoProfissional' , 'numeroConselhoProfissional',
                                            'UF', 'CBOS', 'indicacaoAcidente', 'dataAtendimento', 'tipoConsulta', 'codigoTabela',
                                            'codigoProcedimento', 'valorProcedimento'
                                        ])
        
        df.to_excel(f'docs\{self.tipo_transacao}-Lote_{self.num_lote}-DataRegistro_{self.data_registro}-RegistroANS_{self.registro_ans}-versaoXml_{self.versao_xml}.xlsx', index=False)
 
class ConversorConsulta(ConversorXml):

    def __init__(self, path: str, lote: dict = {'ans': "http://www.ans.gov.br/padroes/tiss/schemas"}) -> None:
        super().__init__(path, lote)

    def carregar_cabecalho_consulta(self,guia):
        dict_cabecalho = self.cria_dicionario(itens=guia,path='ans:cabecalhoConsulta//')
        return dict_cabecalho
        
    def carregar_numero_guia_operadora(self, guia):
        dict_num_guia_operadora = self.cria_dicionario(itens=guia,path='ans:numeroGuiaOperadora')
        return dict_num_guia_operadora

    def carregar_dados_beneficiario(self,guia):
        dict_dados_beneficiario = self.cria_dicionario(itens=guia,path='ans:dadosBeneficiario//')
        return dict_dados_beneficiario

    def carregar_contratado_executante(self,guia):
        dict_contratado_executante = self.cria_dicionario(itens=guia,path='ans:contratadoExecutante//')
        return dict_contratado_executante

    def carregar_profissional_executante(self,guia):
        dict_profissional_executante = self.cria_dicionario(itens=guia,path='ans:profissionalExecutante//')
        return dict_profissional_executante
    
    def carregar_indicacao_acidente(self,guia):
        dict_indicacao_acidente = self.cria_dicionario(itens=guia,path='ans:indicacaoAcidente')
        return dict_indicacao_acidente

    def carregar_dados_atendimento(self,guia):
        dict_dados_atendimento = self.cria_dicionario(itens=guia,path="ans:dadosAtendimento//")
        return dict_dados_atendimento

    def carregar_guias(self) -> list:
        header = self.carregar_cabecalho()
        lista = []
        
        guias = self.eroot.findall('.//ans:guiaConsulta', self.lote)
        for guia in guias:
            dicionario = {}

            dicionario.update(header)
            
            cabecalho = self.carregar_cabecalho_consulta(guia=guia)
            dicionario.update(cabecalho)

            num_guia = self.carregar_numero_guia_operadora(guia=guia)
            dicionario.update(num_guia)

            dados_beneficiario = self.carregar_dados_beneficiario(guia=guia)
            dicionario.update(dados_beneficiario)

            contratado_executante = self.carregar_contratado_executante(guia=guia)
            dicionario.update(contratado_executante)

            profissional_executante = self.carregar_profissional_executante(guia=guia)
            dicionario.update(profissional_executante)

            indicacao_acidente = self.carregar_indicacao_acidente(guia=guia)
            dicionario.update(indicacao_acidente)

            dados_atendimento = self.carregar_dados_atendimento(guia=guia)
            dicionario.update(dados_atendimento)
            
            lista.append(dicionario)
        
        return lista

    def salvar_excel(self):

        guias = self.carregar_guias()


        df = pd.DataFrame(guias)
        
        tipo_transacao = df.tipoTransacao[0]
        num_lote = df.sequencialTransacao[0]
        data_registro = df.dataRegistroTransacao[0]

        df.to_excel(f'docs\Consultas\{tipo_transacao}-Lote_{num_lote}-DataRegistro_{data_registro}.xlsx', index=False)

class ConversorSADT(ConversorXml):
    def __init__(self, path: str, lote: dict = {'ans':"http://www.ans.gov.br/padroes/tiss/schemas"}) -> None:
        super().__init__(path, lote)

    def carregar_cabecalho_sadt(self,guia):
        dict_cabecalho = self.cria_dicionario(itens=guia,path='ans:cabecalhoGuia//')
        return dict_cabecalho

    def carregar_dados_autorizacao(self,guia):
        dict_autorizacao = self.cria_dicionario(itens=guia, path='ans:dadosAutorizacao//')
        return dict_autorizacao
    
    def carregar_dados_beneficiario(self,guia):
        dict_beneficiario = self.cria_dicionario(itens=guia,path='ans:dadosBeneficiario//')
        return dict_beneficiario
    
    def carregar_dados_solicitante(self,guia):
        dict_solicitante = self.cria_dicionario(itens=guia,path='ans:dadosSolicitante//')
        return dict_solicitante
    
    def carregar_dados_solicitacao(self,guia):
        dict_solicitacao = self.cria_dicionario(itens=guia,path='ans:dadosSolicitacao//')
        return dict_solicitacao
    
    def carregar_dados_executante(self,guia):
        dict_executante = self.cria_dicionario(itens=guia,path='ans:dadosExecutante//')
        return dict_executante
    
    def carregar_dados_atendimento(self,guia):
        dict_atendimento = self.cria_dicionario(itens=guia,path='ans:dadosAtendimento//')
        return dict_atendimento
    
    def carregar_dados_procedimento(self,guia):
        dict_procedimento = self.cria_dicionario(itens=guia,path='ans:procedimentosExecutados//')
        return dict_procedimento
    
    def carregar_outras_despesas(self,guia):
        dict_despesas = self.cria_dicionario(itens=guia,path='ans:outrasDespesas//')
        return dict_despesas
    
    def carregar_valor(self,guia):
        dict_valor = self.cria_dicionario(itens=guia,path='ans:valorTotal//')
        return dict_valor
    
    def carregar_guias(self) -> list:
        header = self.carregar_cabecalho()
        lista = []

        guias = self.eroot.findall('.//ans:guiaSP-SADT', self.lote)

        for guia in guias:
            dicionario = {}

            dicionario.update(header)

            cabecalho = self.carregar_cabecalho_sadt(guia=guia)
            dicionario.update(cabecalho)

            autorizacao = self.carregar_dados_autorizacao(guia=guia)
            dicionario.update(autorizacao)

            beneficiario = self.carregar_dados_beneficiario(guia=guia)
            dicionario.update(beneficiario)

            solicitante = self.carregar_dados_solicitante(guia=guia)
            dicionario.update(solicitante)

            solicitacao = self.carregar_dados_solicitacao(guia=guia)
            dicionario.update(solicitacao)

            executante = self.carregar_dados_executante(guia=guia)
            dicionario.update(executante)

            atendimento = self.carregar_dados_atendimento(guia=guia)
            dicionario.update(atendimento)

            procedimento = self.carregar_dados_procedimento(guia=guia)
            dicionario.update(procedimento)

            despesas = self.carregar_outras_despesas(guia=guia)
            dicionario.update(despesas)

            valor = self.carregar_valor(guia=guia)
            dicionario.update(valor)

            lista.append(dicionario)
        
        return lista

    def salvar_excel(self):
        
        guias = self.carregar_guias()

        df = pd.DataFrame(guias)

        tipo_transacao = df.tipoTransacao[0]
        num_lote = df.sequencialTransacao[0]
        data_registro = df.dataRegistroTransacao[0]

        df.to_excel(f'docs\SADT\{tipo_transacao}-Lote_{num_lote}-DataRegistro_{data_registro}.xlsx', index=False)

class ConversorHonorario(ConversorXml):
    def __init__(self, path: str, lote: dict = { 'ans': "http://www.ans.gov.br/padroes/tiss/schemas" }) -> None:
        super().__init__(path, lote)

    def carregar_cabecalho_honorario(self,guia):
        dict_cabecalho = self.cria_dicionario(itens=guia,path='ans:cabecalhoGuia//')
        return dict_cabecalho
    
    def carregar_guiaSolicitacao(self,guia):
        dict_solicitacao = self.cria_dicionario(itens=guia,path='ans:guiaSolicInternacao')
        return dict_solicitacao

    def carregar_senha(self,guia):
        dict_senha = self.cria_dicionario(itens=guia,path='ans:senha')
        return dict_senha
    
    def carregar_numero_guia(self,guia):
        dict_num = self.cria_dicionario(itens=guia,path='ans:numeroGuiaOperadora')
        return dict_num
    
    def carregar_beneficiario(self,guia):
        dict_beneficiario = self.cria_dicionario(itens=guia,path='ans:beneficiario//')
        return dict_beneficiario
    
    def carregar_local_contratado(self,guia):
        dict_local = self.cria_dicionario(itens=guia,path='ans:localContratado//')
        return dict_local
    
    def carregar_dados_executante(self,guia):
        dict_executante = self.cria_dicionario(itens=guia,path='ans:dadosContratadoExecutante//')
        return dict_executante
    
    def carregar_dados_internacao(self,guia):
        dict_internacao = self.cria_dicionario(itens=guia,path='ans:dadosInternacao//')
        return dict_internacao
    
    def carregar_procedimento(self,guia):
        dict_procedimento = self.cria_dicionario(itens=guia,path='ans:procedimentosRealizados//')
        return dict_procedimento

    def carregar_valor(self,guia):
        dict_valor = self.cria_dicionario(itens=guia,path='ans:valorTotalHonorarios')
        return dict_valor
    
    def carregar_emissao(self,guia):
        dict_emissao = self.cria_dicionario(itens=guia,path='ans:dataEmissaoGuia')
        return dict_emissao
    
    def carregar_guias(self) -> list:
        header = self.carregar_cabecalho()
        lista = []

        guias = self.eroot.findall('.//ans:guiaHonorarios', self.lote)

        for guia in guias:
            dicionario = {}

            dicionario.update(header)

            cabecalho = self.carregar_cabecalho_honorario(guia=guia)
            dicionario.update(cabecalho)

            solicitacao = self.carregar_guiaSolicitacao(guia=guia)
            dicionario.update(solicitacao)

            senha = self.carregar_senha(guia=guia)
            dicionario.update(senha)

            try:
                num_guia = self.carregar_numero_guia(guia=guia)
                dicionario.update(num_guia)
            except:
                pass
            
            beneficiario = self.carregar_beneficiario(guia=guia)
            dicionario.update(beneficiario)

            contratado = self.carregar_local_contratado(guia=guia)
            dicionario.update(contratado)

            executante = self.carregar_dados_executante(guia=guia)
            dicionario.update(executante)

            internacao = self.carregar_dados_internacao(guia=guia)
            dicionario.update(internacao)

            procedimento = self.carregar_procedimento(guia=guia)
            dicionario.update(procedimento)

            valor = self.carregar_valor(guia=guia)
            dicionario.update(valor)

            emissao = self.carregar_emissao(guia=guia)
            dicionario.update(emissao)


            lista.append(dicionario)
        
        return lista          
    
    def salvar_excel(self):

        guias = self.carregar_guias()

        df = pd.DataFrame(guias)

        tipo_transacao = df.tipoTransacao[0]
        num_lote = df.sequencialTransacao[0]
        data_registro = df.dataRegistroTransacao[0]

        df.to_excel(f'docs\Honorario\{tipo_transacao}-Lote_{num_lote}-DataRegistro_{data_registro}.xlsx', index=False)

