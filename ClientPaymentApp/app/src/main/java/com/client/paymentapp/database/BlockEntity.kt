package com.client.paymentapp.database

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "blocks")
data class BlockEntity(
    val tokenID: String,
    val senderID: String,
    val receiverID: String,
    val senderNonce: Int,
    val receiverNonce: Int,
    @PrimaryKey val hash: String,
    val previousHash: String,
    val senderSignature: String,
    val receiverSignature: String
)
