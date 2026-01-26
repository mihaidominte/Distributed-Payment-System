package com.client.paymentapp.database

import androidx.room.*

@Dao
interface UserDAO {

    @Query("SELECT * FROM user LIMIT 1")
    suspend fun getUser(): UserEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(user: UserEntity)

    @Query("UPDATE user SET balance = :newAmount")
    suspend fun updateBalance(newAmount: Double)

    @Query("""
        UPDATE user 
        SET privateKey = :newPrivateKey,
            publicKey = :newPublicKey
    """)
    suspend fun updateKeys(
        newPrivateKey: String,
        newPublicKey: String
    )

    @Query("UPDATE user SET serverPublicKey = :serverKey")
    suspend fun updateServerPublicKey(serverKey: String)
}
