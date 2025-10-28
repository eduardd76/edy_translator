const { AccessToken } = require('livekit-server-sdk');

exports.handler = async (event, context) => {
    // Only allow POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const apiKey = process.env.LIVEKIT_API_KEY;
        const apiSecret = process.env.LIVEKIT_API_SECRET;
        const livekitUrl = process.env.LIVEKIT_URL;

        if (!apiKey || !apiSecret || !livekitUrl) {
            throw new Error('Missing LiveKit configuration');
        }

        // Generate unique room name
        const roomName = `edy-${Date.now()}-${Math.random().toString(36).substring(7)}`;
        const participantName = `user-${Math.random().toString(36).substring(7)}`;

        // Create access token
        const at = new AccessToken(apiKey, apiSecret, {
            identity: participantName,
        });

        at.addGrant({
            room: roomName,
            roomJoin: true,
            canPublish: true,
            canSubscribe: true,
        });

        const token = await at.toJwt();

        // Trigger Azure Container App (optional - if you want to wake it up)
        // This is where you'd call Azure to ensure the agent is running
        // For scale-to-zero, the agent should auto-connect when it detects the room

        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify({
                token,
                url: livekitUrl,
                roomName,
            })
        };

    } catch (error) {
        console.error('Error generating token:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ 
                error: 'Failed to generate token',
                message: error.message 
            })
        };
    }
};
