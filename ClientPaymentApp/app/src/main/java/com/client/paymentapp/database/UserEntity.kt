package com.client.paymentapp.database

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "user")
data class UserEntity(
    @PrimaryKey val id: String,
    val password: String,
    val balance: Double,
    val privateKey: String,
    val publicKey: String,
    val serverPublicKey: String
)
