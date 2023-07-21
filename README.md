# API para consultar GPT usando Durable Function para extraer información de las Fare Rules de TP Travel

_La API recibe un Json con el texto a ser analizado y retorna la respuesta del modelo GPT, de OPENAI_

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

    git clone https://fecork@bitbucket.org/onetp/spf_iamodel_tptravel.git


esto descargará el código del repositorio
	
	https://bitbucket.org/onetp/spf_iamodel_tptravel/src/master/
Mira **Deployment** para conocer como desplegar el proyecto.

### Pre-requisitos 📋

Instalar

- [Azure Function Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash)
- [Extensión Azure Function para Visual Studio](https://github.com/microsoft/vscode-azurefunctions)

### Instalación 🔧

Para ejecutar en local

```
pip install -r requirements.txt
```

En Azure las librerías se instalan automaticamente

## Ejecutando ⚙️

```
func host start
```

## API 🦉

consultar al modelo en las rutas

### Develop
	https://tptravel-gptmodel.azurewebsites.net/api/GptModelPoliciesTpt?


### QA

	https://aznprd-eus-trqa-func02.azurewebsites.net/api/GptModelPoliciesTpt?


### Production

### Expedia
	
	https://azprd-eus-tvex-func01.azurewebsites.net/api/GptModelPoliciesTpt?

	

### Aeroméxico

	https://azprd-eus-trpr-func01.azurewebsites.net/api/GptModelPoliciesTpt


Recibe el objeto Json

```json
    {
        "task": str,
		"information": [objects],
		"penaltyText": [objects],

    }
```

para ver un ejemplo completo, puede ver el archivo

	test.json

donde:

- Task: string con la tarea a ejecutar: CANCELLATION, CHANGE, AVAILABILITY, FUELSURCHARGE, DEPARTUREDATE

```json
 "task": "CANCELLATION"
```

CANCELLATION: para esta tarea, el modelo revisará la categoría 16, en caso de existir un menor de edad, la categoría 16 y 19, la Cancelación para Aeroméxico es CANCELLATIONMX

CHANGE: para esta tarea, el modelo revisará la categoría 16. para Aeroméxico es CHANGEMX

AVAILABILITY: para cambios manuales, el modelo revisará la categoría 2, 3, 4, 6, 7, 8, 10, 11.

FUELSURCHARGES: para combustible, el modelo revisará la categoría 12

DEPARTUREDATE: para cargos sobre el origen y
fecha de salida del vuelo, el modelo revisa la
categoría 12

TIME: revisa la categoría 16 en busca del lugar, fecha y hora de vuelo

ENDORSEMENTS: analiza la categoría 18

TICKETINGCHARGE: analiza la categoría 12, para buscar cargos de acuerdo a la fecha de salida.

ADDITIONALCHARGE: analiza la categoría 12, para buscar número, hora, día del vuelo y encontrar cargos respectivos


para conocer en detalle las preguntas para cada categoría, revisar el archivo:

	conf\base\parameters\questions_database_lite.yml


- Information: string de la información del ticket: fareBasis, origin, date departure, información de menor de edad, etc

por ejemplo

```json
    "information": {
        "departureDate": "2023-01-05T06:00:00",
        "passengerChild": [
            {
                "age": 8,
                "seat": true,
				"isAccompanied": true
            },
            {
                "age": 2,
                "seat": false,
				"isAccompanied": false
            }
        ]
    },
```

- Rules: string de la clase con las reglas correspondiente, se reciben las 33 categorias, por ejemplo para cancelación es la clase 16 y 19

```json
"penaltyText":[
    {
      "fareBasis": "KLEQPZ0K",
      "categories": [
        {
          "code": "16",
          "freeText": "CHANGES\nANY TIME\nCHANGES NOT PERMITTED IN CASE OF REISSUE/\nREVALIDATION.\nANY TIME\nCHANGES NOT PERMITTED IN CASE OF NO-SHOW.\nNOTE"
		  "name":"Penalties"
		}
		{
		 "code":"19",
		 "freeText":
		 "name":
		}
```

el modelo GPT responderá:

- question: pregunta que se realiza acerca de las reglas entregadas.
- quote: parrafo o texto de donde extrajo la respuesta.
- answer: respuesta del modelo
- boolean: para indicar con True o False si el modelo encontró una respuesta.
- category: para indicar de que categoría extrajo la respuesta
- meanProbability: indica la probabilidad media de generación de cada token en la respuesta

```json
  			{
				"question": str,
				"answer": [str],
				"category": int,
				"quote": str,
				"freeText": boolean,
				"number_question": int,
				"boolean": boolean,
				"meanProbability":float,
				"value": [float],
				"denomination": [str]
			},
```

Por ejemplo:

```json
  {
				"question": "\n\"3. How much is THE FEE FOR NO-SHOW.\"\n",
				"answer": [
					"FEE ___ FOR NO SHOW"
				],
				"category": 16,
				"quote": "TICKET IS NON-REFUNDABLE IN CASE OF CANCEL/REFUND.",
				"freeText": true,
				"number_question": 3,
				"boolean": false,
				"meanProbability": 98.45931417035175,
				"value": [],
				"denomination": []
			},
```

para las preguntas, en donde se extrae valores de moneda, como por ejemplo la question_3 se entrega además:

- value: valor flotante con el cargo encontrado
- denomination: moneda o denominación del cargo: USD, JPY, GBP

por ejemplo.

```json
	"question_3": {
		"answer": ["USD 200.00"],
		"quote": "CHARGE USD 200.00 FOR CANCEL.",
		"boolean": true,
		"question": "How much is the CHARGE FOR CANCEL?",
		"Value": [200.0],
		"Denomination": ["USD"]
	},
```

## Tener en cuenta

- el tiempo de respuesta depende de la cantidad de texto, las categorias que más suelen demorar son la 12, 16 y 19
- GPT 3 puede procesar solamente 4000 tokens, aproxímadamente unas 3000 palabras

## Despliegue 📦

El código se encuentra desplegado en las siguientes Azure Function.

### Desarrollo

```
tptravel-model
```

del grupo de recursos

```
TPTravelDEV12901
```

de la suscripción

```
Teleperformance Colombia
```

### QA

```
aznprd-eus-trqa-func02
```

del grupo de recursos

```
aznprd-eus-trqa-rg
```

de la suscripción

```
TP Global Non-Production
```

### Producción

Expedia
---
```
azprd-eus-tvex-func01
```

del grupo de recursos

```
azprd-eus-tvex-rg01
```

de la suscripción

```
TP Global Production
```

Aeroméxico
---

	azprd-eus-trpr-func01

del grupo de recursos

```
azprd-eus-trpr-rg
```

de la suscripción

```
TP Global Production
```

Los guías usadas para desplegar son:

[Visual Studio Code](https://fecork.notion.site/Desplegar-c-digo-en-Azure-Function-con-Visual-Studio-Code-df55f8a586af43709ef499ab4dc298c4)

[Pipeline](https://fecork.notion.site/Pipeline-para-Azure-Function-4a46b6b2529a4311841d6a51516ecf2a)

[Release](https://fecork.notion.site/Release-para-Azure-Function-3203b3a312aa40a79c2074533fc252d5)

## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

- [Azure Functions SDK](https://pypi.org/project/azure-functions/) - Microsoft
- [OpenAI API](https://openai.com/blog/openai-api/) - Modelo GPT3
- [Spacy](https://spacy.io) - Librería para procesar texto

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

## Autores ✒️

_Menciona a todos aquellos que ayudaron a levantar el proyecto desde sus inicios_


- **Jackeline Gomez** [LinkenId](https://www.linkedin.com/in/jackeline-g%C3%B3mez-londo%C3%B1o-97aa66204/)

- **Mariana Jaramillo** [LinkenId](https://www.linkedin.com/in/mariana-jaramillo-acero-114b55234/)

- **Wilberth Ferney Córdoba Canchala** - [LinkenId](https://www.linkedin.com/in/wilberth-ferney-córdoba-canchala-9734b74b/)


## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

## Expresiones de Gratitud 🎁

- Comenta a otros sobre este proyecto 📢
- Invita una cerveza 🍺 o un café ☕ a alguien del equipo.
- Da las gracias públicamente 🤓.
- etc.
