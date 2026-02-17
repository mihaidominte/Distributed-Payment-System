package com.client.paymentapp.network

import kotlinx.coroutines.*
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.PrintWriter
import java.net.Socket

class Client() {

    private var socket: Socket? = null
    private var writer: PrintWriter? = null
    private var reader: BufferedReader? = null

    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    private var pendingResponse: CompletableDeferred<String>? = null

    suspend fun connect(
        host: String = "192.168.0.104",
        port: Int = 9999) = withContext(Dispatchers.IO) {

        if (socket?.isConnected == true) return@withContext

        socket = Socket(host, port)
        writer = PrintWriter(socket!!.getOutputStream(), true)
        reader = BufferedReader(InputStreamReader(socket!!.getInputStream()))

        scope.launch {
            try {
                while (isActive) {
                    val line = reader?.readLine() ?: break
                    pendingResponse?.complete(line)
                }
            } catch (_: Exception) {
            }
        }
    }

    suspend fun sendAndWait(
        json: JSONObject,
        timeoutMillis: Long = 30_000
    ): JSONObject = withContext(Dispatchers.IO) {

        if (writer == null) {
            throw IllegalStateException("Not connected")
        }

        val deferred = CompletableDeferred<String>()
        pendingResponse = deferred
        writer!!.println(json.toString())

        try {
            val response = withTimeout(timeoutMillis) {
                deferred.await()
            }
            JSONObject(response)
        } finally {
            pendingResponse = null
        }
    }


    fun disconnect() {
        scope.cancel()
        writer?.close()
        reader?.close()
        socket?.close()

        writer = null
        reader = null
        socket = null
    }
}
