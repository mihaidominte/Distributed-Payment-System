package com.client.paymentapp

import android.util.Base64
import java.security.KeyFactory
import java.security.KeyPair
import java.security.KeyPairGenerator
import java.security.PrivateKey
import java.security.PublicKey
import java.security.Signature
import java.security.spec.PKCS8EncodedKeySpec
import java.security.spec.X509EncodedKeySpec

object Utils {

    fun generateKeyPair(): GeneratedKeys {
        val generator = KeyPairGenerator.getInstance("RSA")
        generator.initialize(2048)

        val keyPair: KeyPair = generator.generateKeyPair()

        return GeneratedKeys(
            privateKey = encode(keyPair.private.encoded),
            publicKey = encode(keyPair.public.encoded)
        )
    }

    fun sign(data: String, privateKeyStr: String): String {
        val privateKey = decodePrivateKey(privateKeyStr)

        val signature = Signature.getInstance("SHA256withRSA")
        signature.initSign(privateKey)
        signature.update(data.toByteArray())

        return encode(signature.sign())
    }

    fun verify(
        data: String,
        signatureStr: String,
        publicKeyStr: String
    ): Boolean {
        val publicKey = decodePublicKey(publicKeyStr)

        val signature = Signature.getInstance("SHA256withRSA")
        signature.initVerify(publicKey)
        signature.update(data.toByteArray())

        return signature.verify(decode(signatureStr))
    }

    private fun decodePrivateKey(key: String): PrivateKey {
        val bytes = decode(key)
        val spec = PKCS8EncodedKeySpec(bytes)
        return KeyFactory.getInstance("RSA").generatePrivate(spec)
    }

    private fun decodePublicKey(key: String): PublicKey {
        val bytes = decode(key)
        val spec = X509EncodedKeySpec(bytes)
        return KeyFactory.getInstance("RSA").generatePublic(spec)
    }

    private fun encode(bytes: ByteArray): String =
        Base64.encodeToString(bytes, Base64.NO_WRAP)

    private fun decode(data: String): ByteArray =
        Base64.decode(data, Base64.NO_WRAP)

    data class GeneratedKeys(
        val privateKey: String,
        val publicKey: String
    )
}
