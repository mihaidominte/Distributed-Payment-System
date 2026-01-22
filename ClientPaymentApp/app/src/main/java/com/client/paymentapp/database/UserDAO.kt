package com.client.paymentapp.database

import androidx.room.*

@Dao
interface UserDAO {
    @Query("SELECT * FROM user WHERE id = 0")
    suspend fun getUser(): UserEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(user: UserEntity)

    @Query("UPDATE user SET balance = :newAmount WHERE id = 0")
    suspend fun updateBalance(newAmount: Double)

    @Query("UPDATE user SET userId = :newUserId WHERE id = 0")
    suspend fun updateUserId(newUserId: String)

    @Query("UPDATE user SET privateKey = :newPrivateKey, " +
            "publicKey = :newPublicKey WHERE id = 0")
    suspend fun updateKeys(newPrivateKey: String, newPublicKey: String)
}