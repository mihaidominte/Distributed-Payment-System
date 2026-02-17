package com.client.paymentapp.network

data class FinalizeConfigRequest(
    val activity: String = "new_user_final_config",
    val id: String,
    val public_key: String
)

