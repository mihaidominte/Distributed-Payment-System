package com.client.paymentapp.database

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.security.MessageDigest

@Entity(tableName = "tokens")
data class TokensEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val senderId: String,
    val receiverId: String,
    val amount: Double,
    val date: Long,
    val hash: String,
    val signature: String,
    val counterpartySignature: String,
    val previousHash: String?
){
    fun computeHash(): String {
        val data = "$previousHash|$senderId|$receiverId|$amount|$date"
        return data.sha256()
    }
}
fun String.sha256(): String {
    val bytes = MessageDigest.getInstance("SHA-256").digest(this.toByteArray())
    return bytes.joinToString("") { "%02x".format(it) }
}