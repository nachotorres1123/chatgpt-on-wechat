# encoding:utf-8

import json
import logging
import os
import pickle

from common.log import logger

# Coloca todas las configuraciones disponibles en un diccionario, por favor utiliza letras minúsculas
# Estos valores de configuración aquí no tienen ningún significado real, el programa no los utilizará aquí, solo son para dar formato y guía, por favor agrega las configuraciones a config.json
configuracion_disponible = {
    # Configuración de la API de OpenAI
    "clave_api_openai": "",  # Clave de la API de OpenAI
    # Apibase de OpenAI, cuando use_azure_chatgpt es verdadero, es necesario configurar la base de la API correspondiente
    "base_api_openai": "https://api.openai.com/v1",
    "proxy": "",  # Proxy utilizado por OpenAI
    # Modelo chatgpt, cuando use_azure_chatgpt es verdadero, el nombre es el nombre de implementación del modelo en Azure
    "modelo": "gpt-3.5-turbo",    # También es compatible con gpt-3.5-turbo-16k, gpt-4, wenxin
    "use_azure_chatgpt": False,  # ¿Utilizar Azure ChatGPT?
    "identificacion_despliegue_azure": "",  # Nombre de implementación en Azure
    "version_api_azure": "",  # Versión de la API de Azure
    # Configuración de activación del bot
    "prefijo_charla_individual": ["bot", "@bot"],  # Para que el bot responda en charlas individuales, el texto debe contener este prefijo
    "prefijo_respuesta_charla_individual": "[bot] ",  # Prefijo para respuestas automáticas en charlas individuales
    "sufijo_respuesta_charla_individual": "",  # Sufijo para respuestas automáticas en charlas individuales, \n representa un cambio de línea
    "prefijo_charla_grupo": ["@bot"],  # Para que el bot responda en charlas grupales, el texto debe contener este prefijo
    "prefijo_respuesta_charla_grupo": "",  # Prefijo para respuestas automáticas en charlas grupales
    "sufijo_respuesta_charla_grupo": "",  # Sufijo para respuestas automáticas en charlas grupales, \n representa un cambio de línea
    "palabras_clave_charla_grupo": [],  # Si el mensaje en el grupo contiene estas palabras clave, el bot responderá
    "desactivar_mencion_grupo": False,  # ¿Desactivar la activación de @bot en charlas grupales?
    "lista_blanca_nombres_grupo": ["ChatGPT Grupo de Prueba", "ChatGPT Grupo de Prueba 2"],  # Lista de nombres de grupos donde las respuestas automáticas están habilitadas
    "lista_blanca_palabras_clave_nombres_grupo": [],  # Lista de palabras clave para nombres de grupos donde las respuestas automáticas están habilitadas
    "lista_compartida_sesiones_grupo": ["ChatGPT Grupo de Prueba"],  # Lista de nombres de grupos con sesiones de conversación compartidas
    "activacion_por_mismo_bot": False,  # ¿Permitir que el bot se active a sí mismo?
    "prefijo_creacion_imagen": ["crear", "ver", "buscar"],  # Prefijo para generar imágenes
    "concurrency_in_session": 1,  # Máximo número de mensajes en una misma sesión en proceso, un valor mayor a 1 puede causar desorden
    "tamano_creacion_imagen": "256x256",  # Tamaño de la imagen, opciones: 256x256, 512x512, 1024x1024
    # Parámetros de la sesión chatgpt
    "caducidad_segundos": 3600,  # Tiempo de caducidad de la sesión sin actividad
    # Descripción de la personalidad
    "descripcion_personalidad": "Eres ChatGPT, un modelo de lenguaje grande entrenado por OpenAI. Tu objetivo es responder y resolver cualquier pregunta de las personas, y puedes comunicarte en varios idiomas.",
    "max_caracteres_conversacion": 1000,  # Máximo número de caracteres para la memoria de la conversación
    # Configuración de limitación de uso de chatgpt
    "limitar_frecuencia_chatgpt": 20,  # Límite de frecuencia de llamadas a chatgpt
    "limitar_frecuencia_dalle": 50,  # Límite de frecuencia de llamadas a OpenAI DALL-E
    # Parámetros de la API de chatgpt, consultar https://platform.openai.com/docs/api-reference/chat/create
    "temperatura": 0.9,
    "top_p": 1,
    "penalizacion_frecuencia": 0,
    "penalizacion_presencia": 0,
    "tiempo_espera_solicitud": 60,  # Tiempo de espera para solicitudes a chatgpt, la configuración predeterminada de la API de OpenAI es 600, problemas difíciles pueden requerir más tiempo
    "tiempo_espera_reintentos": 120,  # Tiempo de espera para reintentos a chatgpt, en este periodo se realizará un reintentos automáticos
    # Parámetros de Baidu Wenxin
    "modelo_baidu_wenxin": "eb-instant", # Modelo Baidu Wenxin utilizado de manera predeterminada
    "clave_api_baidu_wenxin": "", # Clave API Baidu
    "clave_secreta_baidu_wenxin": "", # Clave secreta API Baidu
    # Configuración de voz
    "reconocimiento_voz": False,  # ¿Habilitar reconocimiento de voz?
    "reconocimiento_voz_grupo": False,  # ¿Habilitar reconocimiento de voz en grupos?
    "usar_voz_respuesta_voz": False,  # ¿Usar voz para respuestas de voz? Es necesario configurar la clave de API correspondiente al motor de síntesis de voz
    "usar_siempre_voz_respuesta": False,  # ¿Usar siempre voz para respuestas?
    "reconocimiento_voz_a_texto": "openai",  # Motor de reconocimiento de voz, opciones: openai, baidu, google, azure
    "texto_a_voz": "baidu",  # Motor de síntesis de voz, opciones: baidu, google, pytts (offline), azure
    # Configuración de la API de voz de Baidu, se requiere cuando se utiliza el reconocimiento y la síntesis de voz de Baidu
    "baidu_app_id": "",
    "
