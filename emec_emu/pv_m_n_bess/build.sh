## Creo la imagen de pydae
docker build -t ingelectus.com/helios/pydae .

docker compose up -d


## Copio tanto la configuracion del controller como la del simulador.
mkdir -p configs
docker cp ppc_pydae:/app/config_controller.json configs/.
docker cp ppc_pydae:/app/config_simulator.json configs/.