from telethon import TelegramClient, events
import stripe

# Your Stripe API keys
stripe.api_key = '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'

# Your Telegram bot token and API credentials
api_id = '10337096'
api_hash = '44eb4f665fe6c15824c5b469d1111424'
bot_token = '7058591192:AAHUc0wnCfYx2ciYHD1R38B3kuVaIvDDmAc'

client = TelegramClient('YOUR_SESSION_NAME', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/check'))
async def check_card(event):
    # Get card details from the user (you'll need to implement this securely)
    card_number = await get_card_number(event) 
    expiry_month = await get_expiry_month(event) 
    expiry_year = await get_expiry_year(event)
    cvv = await get_cvv(event) 

    try:
        # Create a Stripe token
        token = stripe.Token.create(
            card={
                'number': card_number,
                'exp_month': expiry_month,
                'exp_year': expiry_year,
                'cvc': cvv
            }
        )

        # Attempt a small charge
        charge = stripe.Charge.create(
            amount=100,  # $1 in cents
            currency='usd',
            source=token.id,
            description='Card check'
        )

        # Check the charge status
        if charge.status == 'succeeded':
            await event.respond('✅ Card is LIVE!')
        else:
            await event.respond(f'❌ Card declined: {charge.outcome.seller_message}')

    except stripe.error.CardError as e:
        await event.respond(f'❌ Card error: {e.error.message}')
    except Exception as e:
        await event.respond(f'⚠️ An error occurred: {e}')

client.run_until_disconnected()
