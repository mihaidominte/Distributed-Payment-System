package com.client.paymentapp.database

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "tokens")
data class TokenEntity(
    @PrimaryKey val id: String,
    val value: Long,
    val bankSignature: String
)