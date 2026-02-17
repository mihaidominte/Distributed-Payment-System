package com.client.paymentapp.network

data class GenericResponse(
    val activity: String,
    val reason: String? = null
)
