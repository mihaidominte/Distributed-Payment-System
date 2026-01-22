package com.client.paymentapp.database

import androidx.room.*

@Dao
interface TokensDAO {
    @Query("SELECT * FROM tokens WHERE id = :id")
    suspend fun getById(id: Int): TokensEntity?

    @Query("SELECT * FROM tokens")
    suspend fun getALL(): List<TokensEntity>

    @Query("SELECT * FROM tokens WHERE hash " +
            "NOT IN (SELECT previousHash FROM tokens) LIMIT 1")
    suspend fun getLastToken(): TokensEntity?

    @Query("SELECT * FROM tokens WHERE senderId = 'Server'")
    suspend fun getServerToken(): TokensEntity?

    @Query("DELETE FROM tokens")
    suspend fun deleteAll()

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(tokens: TokensEntity)
}