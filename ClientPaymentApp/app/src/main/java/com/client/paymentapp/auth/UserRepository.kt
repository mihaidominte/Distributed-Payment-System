package com.client.paymentapp.auth

import android.content.Context
import com.client.paymentapp.Utils
import com.client.paymentapp.database.DatabaseProvider
import com.client.paymentapp.database.UserEntity
import com.client.paymentapp.network.Client
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.security.MessageDigest
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

object UserRepository {

    private const val SERVER_ADDRESS = "10.0.2.2"
    private const val SERVER_PORT = 9000


    suspend fun hasUser(context: Context): Boolean = withContext(Dispatchers.IO) {
        DatabaseProvider
            .getDatabase(context)
            .userDao()
            .getUser() != null
    }

    suspend fun login(context: Context, password: String): Boolean = withContext(Dispatchers.IO) {
        val userDao = DatabaseProvider.getDatabase(context).userDao()
        val user = userDao.getUser() ?: return@withContext false
        return@withContext user.password == hashPassword(password)
    }


    suspend fun checkPassword(
        context: Context,
        password: String
    ): Boolean = withContext(Dispatchers.IO) {
        val user = DatabaseProvider
            .getDatabase(context)
            .userDao()
            .getUser() ?: return@withContext false

        user.password == hashPassword(password)
    }


    suspend fun createUser(
        context: Context,
        password: String
    ) = withContext(Dispatchers.IO) {

        val userDao = DatabaseProvider.getDatabase(context).userDao()
        val client = Client(SERVER_ADDRESS, SERVER_PORT)

        val serverConfig = startUserConfig(client)
        val keyPair = Utils.generateKeyPair()

        val user = UserEntity(
            id = serverConfig.userId,
            password = hashPassword(password),
            balance = 0.0,
            privateKey = keyPair.privateKey,
            publicKey = keyPair.publicKey,
            serverPublicKey = serverConfig.serverPublicKey
        )

        userDao.insert(user)

        finalizeUserConfig(
            client,
            serverConfig.userId,
            keyPair.publicKey
        )

        client.disconnect()
    }


    private suspend fun startUserConfig(
        client: Client
    ): ServerConfig =
        suspendCancellableCoroutine { cont ->

            client.connect(
                onMessage = { msg ->
                    try {
                        val json = JSONObject(msg)
                        if (json.getString("activity") == "config_id") {
                            cont.resume(
                                ServerConfig(
                                    userId = json.getString("id"),
                                    serverPublicKey = json.getString("public_key")
                                )
                            )
                        }
                    } catch (e: Exception) {
                        // ignore malformed packets
                    }
                },
                onError = { err ->
                    cont.resumeWithException(RuntimeException(err))
                }
            )

            val request = JSONObject()
                .put("activity", "new_user_start_config")

            client.send(request.toString())
        }

    private suspend fun finalizeUserConfig(
        client: Client,
        userId: String,
        publicKey: String
    ) = suspendCancellableCoroutine<Unit> { cont ->

        val request = JSONObject()
            .put("activity", "new_user_final_config")
            .put("id", userId)
            .put("public_key", publicKey)

        client.send(request.toString())
        cont.resume(Unit)
    }


    private fun hashPassword(password: String): String {
        val digest = MessageDigest.getInstance("SHA-256")
        return digest.digest(password.toByteArray())
            .joinToString("") { "%02x".format(it) }
    }

    private data class ServerConfig(
        val userId: String,
        val serverPublicKey: String
    )
}
