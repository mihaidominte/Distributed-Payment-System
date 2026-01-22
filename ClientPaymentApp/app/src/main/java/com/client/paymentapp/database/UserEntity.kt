package com.client.paymentapp.database

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "user")
data class UserEntity(
    @PrimaryKey val id: Int = 0,
    val userId: String,
    val balance: Double,
    val privateKey: String,
    val publicKey: String
)
