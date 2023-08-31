*** DESCRIÇÃO DA POC ***
# connect_mqtt() / on_connect:
  - Conexão com o broker do Projeto;
# on_message():
  - Recebe payload JSON via broker;
# convert_to_table():
  - Transforma o payload e cria uma lista de armazenamento (payload_lst);
  - Cria DF para armazenamento final;
  - Cria DF temporário para normalizar os dados da lista + 'árvore' de sensores;
  - Estrutura o DF repassando quais campos do JSON pertencem à quais colunas;
  - Concatena o DF temp + DF final ordenando as colunas


*** ENTRADA DO JSON ATRAVÉS DO BROKER ***
{
    "deviceid":"id-do-dispositivo",
    "fw_ver":"1",
    "timestamp":1693488129,
    "sensors":
    [
        {
            "code":"code",
            "mod_id":1,
            "data":
            [
                {
                    "id_unit":1,
                    "value":0.000
                }
            ]
        }
    ]
}


*** SAÍDA DO DF PARA ARMAZENAMENTO NO DB ***
deviceid            fw_ver          timestamp           sensor_code         sensor_mod_id           id_unit         value
id-do-dispositivo   1               1693488129          code                1                       1               0.000