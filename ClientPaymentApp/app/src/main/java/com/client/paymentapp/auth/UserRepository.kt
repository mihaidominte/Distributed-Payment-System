package com.client.paymentapp.auth

import android.content.Context
import com.client.paymentapp.Utils
import com.client.paymentapp.database.DatabaseProvider
import com.client.paymentapp.database.UserEntity
import com.client.paymentapp.network.ApiClient
import com.client.paymentapp.network.FinalizeConfigRequest
import com.client.paymentapp.network.StartConfigRequest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.security.MessageDigest

object UserRepository {


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

    suspend fun createUser(
        context: Context,
        password: String
    ) = withContext(Dispatchers.IO) {

        val userDao = DatabaseProvider.getDatabase(context).userDao()
        val startResponse = ApiClient.api.startConfig(
            StartConfigRequest()
        )
        val keyPair = Utils.generateKeyPair()

        val user = UserEntity(
            id = startResponse.id,
            password = hashPassword(password),
            balance = 0.0,
            privateKey = keyPair.privateKey,
            publicKey = keyPair.publicKey,
            serverPublicKey = startResponse.public_key
        )

        userDao.insert(user)

        val finalizeResponse = ApiClient.api.finalizeConfig(
            FinalizeConfigRequest(
                id = startResponse.id,
                public_key = keyPair.publicKey
            )
        )

        if (finalizeResponse.activity != "success") {
            throw IllegalStateException("Server config failed")
        }
    }

    private fun hashPassword(password: String): String {
        val digest = MessageDigest.getInstance("SHA-256")
        return digest.digest(password.toByteArray())
            .joinToString("") { "%02x".format(it) }
    }

    suspend fun deleteUser(context: Context) = withContext(Dispatchers.IO) {
        DatabaseProvider
            .getDatabase(context)
            .userDao()
            .deleteUser()
    }

}
