package com.client.paymentapp.network

import kotlinx.coroutines.*
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.PrintWriter
import java.net.Socket

class Client(
    private val address: String,
    private val port: Int
) {

    private var socket: Socket? = null
    private var writer: PrintWriter? = null
    private var reader: BufferedReader? = null

    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    fun connect(onMessage: (String) -> Unit, onError: (String) -> Unit) {
        scope.launch {
            try {
                socket = Socket(address, port)
                writer = PrintWriter(socket!!.getOutputStream(), true)
                reader = BufferedReader(InputStreamReader(socket!!.getInputStream()))

                listenForMessages(onMessage)

            } catch (e: Exception) {
                onError("Connection error: ${e.message}")
            }
        }
    }

    fun send(message: String) {
        scope.launch {
            try {
                val json = JSONObject(message)
                json.put("password", "1234")
                writer?.println(json.toString())
            } catch (e: Exception) {
                writer?.println(message)
            }
        }
    }


    private suspend fun listenForMessages(onMessage: (String) -> Unit) {
        withContext(Dispatchers.IO) {
            try {
                var line: String?
                while (true) {
                    line = reader?.readLine() ?: break
                    onMessage(line)
                }
            } catch (e: Exception) {
                onMessage("Disconnected: ${e.message}")
            }
        }
    }

    fun disconnect() {
        scope.cancel()
        writer?.close()
        reader?.close()
        socket?.close()
    }
}
