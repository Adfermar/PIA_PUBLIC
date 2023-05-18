package com.example.dialog_flow_with_speechtotext;

import static android.speech.tts.TextToSpeech.SUCCESS;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.api.gax.core.FixedCredentialsProvider;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.cloud.dialogflow.v2.DetectIntentRequest;
import com.google.cloud.dialogflow.v2.DetectIntentResponse;
import com.google.cloud.dialogflow.v2.QueryInput;
import com.google.cloud.dialogflow.v2.SessionName;
import com.google.cloud.dialogflow.v2.SessionsClient;
import com.google.cloud.dialogflow.v2.SessionsSettings;
import com.google.cloud.dialogflow.v2.TextInput;
import com.google.common.collect.Lists;
import com.google.protobuf.Struct;
import com.google.protobuf.Value;

import java.io.InputStream;
import java.util.List;
import java.util.Locale;
import java.util.UUID;


import java.time.LocalDateTime;
import java.time.OffsetDateTime;
import java.time.format.DateTimeFormatter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity {

    Button btStart;
    Button btStop;
    TextView tvResponseFromUser;
    TextView tvResponseFromDialogFlow;
    SessionsClient sessionClient;
    SessionName sessionName;
    final static String UNIQUE_UUID = UUID.randomUUID().toString();

    // ---------------------
    // TEXT to SPEECH ADDON
    boolean flagStop = false;
    TextToSpeech tts;
    // ---------------------
    // SPEECH to TEXT ADDON
    ActivityResultLauncher<Intent> sttLauncher;
    Intent sttIntent;
    // ---------------------

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        init();
    }

    //
    private ActivityResultLauncher<Intent> getSttLauncher() {
        return registerForActivityResult(
                new ActivityResultContracts.StartActivityForResult(),
                result -> {
                    String text = "Ups";
                    if(result.getResultCode() == Activity.RESULT_OK) {
                        List<String> r = result.getData().getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                        text = r.get(0);
                        // ------------------------
                        // SPEECH to SPEECH
                        sendToDialogFlow(text);
                        // ------------------------
                    } else if(result.getResultCode() == Activity.RESULT_CANCELED) {
                        text = "Error";
                    }
                    //showAndTalkResult(text);
                }
        );
    }

    private Intent getSttIntent() {
        Intent intencionSpeechToText = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intencionSpeechToText.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intencionSpeechToText.putExtra(RecognizerIntent.EXTRA_LANGUAGE, new Locale("spa", "ES"));
        intencionSpeechToText.putExtra(RecognizerIntent.EXTRA_PROMPT, "Por favor, hable ahora.");
        intencionSpeechToText.putExtra(RecognizerIntent.EXTRA_RESULTS, new String[] {"prueba"});
        return intencionSpeechToText;
    }
    private void initSpeechToText() {
        sttLauncher.launch(sttIntent);
    }
    // -------------------------------------------------------------------

    private void init() {
            btStart = findViewById(R.id.btStart);
            btStop = findViewById(R.id.btStop);
            tvResponseFromUser = findViewById(R.id.tvResponseFromUser);
            tvResponseFromDialogFlow = findViewById(R.id.tvResponseFromDialogFlow);
            sttLauncher = getSttLauncher();
            sttIntent = getSttIntent();
            // -------------------------------------------------------------------
            // SPEECH to SPEECH ADDON
            btStart.setEnabled(true);
            btStop.setEnabled(false);
            // -----------------------
            btStop.setOnClickListener((v -> {
                showMessage("Programa finalizado");
                timer(2000);
                btStart.setEnabled(false);
                btStop.setEnabled(false);
                flagStop = true;
                // =====================
                finish(); // Stop the program and quit the app
                // =====================
            }));
        if(!flagStop) {
            // -----------------------
            tts = new TextToSpeech(this, status -> {
                if (status == SUCCESS) {
                    flagStop = false;
                    tts.setLanguage(new Locale("spa", "ES"));
                    if (setupDialogFlowClient()) {
                        btStart.setOnClickListener((v -> {
                            initSpeechToText();
                            btStart.setEnabled(false);
                            btStop.setEnabled(true);
                        }));
                    } else {
                        btStart.setEnabled(false);
                        btStop.setEnabled(false);
                    }
                }
            });
        }
    }

    private void sendToDialogFlow(String text) {
        // Si el texto NO está vacío
        if(!text.isEmpty()) {
            // enviar el texto usando el cliente de sesión
            sendMessageToBot(text);
        } else {
            Toast.makeText(this, "No puede dejar el campo vacío", Toast.LENGTH_SHORT).show();
        }
    }

    private boolean setupDialogFlowClient() {
        boolean value = true;
        try {
            InputStream stream = this.getResources().openRawResource(R.raw.client_key);
            GoogleCredentials credentials = GoogleCredentials.fromStream(stream)
                    .createScoped(Lists.newArrayList("https://www.googleapis.com/auth/cloud-platform"));
            String projectId = ((ServiceAccountCredentials) credentials).getProjectId();
            SessionsSettings.Builder settingsBuilder = SessionsSettings.newBuilder();
            SessionsSettings sessionsSettings = settingsBuilder.setCredentialsProvider(
                    FixedCredentialsProvider.create(credentials)).build();
            sessionClient = SessionsClient.create(sessionsSettings);
            sessionName = SessionName.of(projectId, UNIQUE_UUID);
        } catch (Exception e) {
            showMessage("\nexception in setupBot: " + e.getMessage() + "\n");
            value = false;
        }
        return value;
    }

    private void showMessage(String message) {
        runOnUiThread(()->{
            tvResponseFromDialogFlow.append(message);
            // ------------------------------------------
            // TEXT to SPEECH ADDON
            tts.speak(message, TextToSpeech.QUEUE_ADD, null, null);
            // ------------------------------------------
        });
    }
/*
    @RequiresApi(api = Build.VERSION_CODES.O)
    private static String parseDate(String date) {
        // -------------------------------------------------------------------
        //String dateTimeString = "2023-05-18T12:00:00+02:00";
        OffsetDateTime offsetDateTime = OffsetDateTime.parse(date);

        // Extrae la fecha y hora local
        LocalDateTime localDateTime = offsetDateTime.toLocalDateTime();

        // Crea un formateador de fecha personalizado
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");

        // Formatea la fecha y hora local en el formato deseado
        return localDateTime.format(formatter);
        // -------------------------------------------------------------------
    }
*/
    private static boolean containsDate(String data) {
        String pattern = "\\b\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\+\\d{2}:\\d{2}\\b";
        Pattern regex = Pattern.compile(pattern);
        Matcher matcher = regex.matcher(data);

        return matcher.find();
    }

    private static String parseDate(String date) {
        LocalDateTime dateTime = null;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            dateTime = LocalDateTime.parse(date, DateTimeFormatter.ISO_OFFSET_DATE_TIME);
        }
        String formattedDate = null;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            formattedDate = dateTime.format(DateTimeFormatter.ofPattern("dd-MM-yyyy"));
        }
        return formattedDate;
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    private static String replaceDateFormatInsideStringText(String data, String type) {
        String pattern="";
        String parsedData = "";
        String matchedData = "";
        String result = data;
        if(type.equals("dia")) {
            pattern = "\\b\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\+\\d{2}:\\d{2}\\b";
        } else {
            // type == "hour"
            pattern = "\\b\\d{2}:\\d{2}:\\d{2}\\b";
        }
        Pattern regex = Pattern.compile(pattern);
        Matcher matcher = regex.matcher(data);
        if (matcher.find()) {
            matchedData = matcher.group();
            if(type.equals("dia")) {
                parsedData = parseDate(matchedData);
            } else {
                parsedData = matchedData.substring(0, 5);
            }
            result = matcher.replaceFirst(parsedData);
        }
        return result;
    }

    public static int calculateNumber(String input) {
        int baseNumber = 1000; // Base number value
        int lengthFactor = 75; // Length factor for linear relation
        int length = input.length();

        int result = baseNumber + length * lengthFactor;
        return result;
    }

    private void timer(Integer wait_time_milis) {
        try {
            Thread.sleep(wait_time_milis);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private void sendMessageToBot(String message) {
        QueryInput input = QueryInput.newBuilder().setText(
                TextInput.newBuilder().setText(message).setLanguageCode("es-ES")).build();
        String text = input.getText().getText();
        // Crear un hilo
        Thread thread = new Thread() {
            @RequiresApi(api = Build.VERSION_CODES.O)
            @Override
            // Enviar el texto. Espero a la respuesta y la transmito
            public void run() {
                try {
                    // Mostramos el mensaje del usuario en el TextView
                    tvResponseFromUser.setText(text);
                    // Crear el objeto de la petición
                    // Enviamos el input creado (con el texto)
                    DetectIntentRequest detectIntentRequest =
                            DetectIntentRequest.newBuilder()
                                    .setSession(sessionName.toString())
                                    .setQueryInput(input)
                                    .build();
                    // Esperamos a obtener la respuesta del DialogFlow
                    DetectIntentResponse detectIntentResponse = sessionClient.detectIntent(detectIntentRequest);
                    // Comprobación
                    if(detectIntentResponse != null) {
                        // Obtenemos tres items de DialogFlow: intent, action y sentiment.
                        // NO SE USAN
                        // intent, action, sentiment, params
                        String action = detectIntentResponse.getQueryResult().getAction();
                        String intent = detectIntentResponse.getQueryResult().getIntent().toString();
                        String sentiment = detectIntentResponse.getQueryResult().getSentimentAnalysisResult().toString();
                        String params = detectIntentResponse.getQueryResult().getParameters().toString();
                        // Campos específicos:
                        String intentName = detectIntentResponse.getQueryResult().getIntent().getDisplayName();
                        boolean endInteraction = detectIntentResponse.getQueryResult().getIntent().getEndInteraction();

                        // Get the "dia" and "hora" values from Dialog-Flow response context
                        Struct parameters = detectIntentResponse.getQueryResult().getParameters();
                        Value diaValue = parameters.getFieldsOrDefault("dia", Value.getDefaultInstance());
                        Value horaValue = parameters.getFieldsOrDefault("hora", Value.getDefaultInstance());

                        String dia = diaValue.getStringValue();
                        String hora = horaValue.getStringValue();

                        // Respuesta obtenida desde DialogFlow
                        String botReply = detectIntentResponse.getQueryResult().getFulfillmentText();

                        // Si la respuesta contiene algún valor mostramos ese mensaje
                        if(!botReply.isEmpty()) {
                            // El usuario quiere salir de la aplicación
                            if (message.equals("salir")) {
                                showMessage("\n\nPrograma finalizado");
                                timer(2000);
                                // =====================
                                finish(); // Stop the program and quit the app
                                // =====================
                            } else {
                                // Comprobamos si la respuesta del bot contiene datos de fecha
                                // y hora
                                if(!dia.isEmpty() & !hora.isEmpty()) {
                                    botReply = replaceDateFormatInsideStringText(botReply, "dia");
                                    botReply = replaceDateFormatInsideStringText(botReply, "hora");
                                }
                                showMessage(botReply + "\n\n");
                                timer(calculateNumber(botReply));
                                // Si el "Intent" está marcado como fin de la interacción
                                // terminamos el programa. Si no lanzamos otra petición de voz
                                if (endInteraction) {
                                    showMessage("\n------------------\nPrograma finalizado");
                                    timer(2000);
                                    finish(); // Stop the program and quit the app
                                } else {
                                    // Launch SPEECH to text again
                                    initSpeechToText();
                                }
                            }
                        } else {
                            showMessage("something went wrong\n");
                        }
                    } else {
                        showMessage("connection failed\n");
                    }
                } catch (Exception e) {
                    showMessage("\nexception in thread: " + e.getMessage() + "\n");
                    e.printStackTrace();
                }
            }
        };

        // Launch main thread
        thread.start();
    }

}
