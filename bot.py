import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random
import string

# ─────────────────────────────────────────────
# SETUP & CONFIGURATION
# ─────────────────────────────────────────────
load_dotenv()
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
BRAND = "Fast Brawl Services"

PAYMENT_DETAILS = {
    "PayPal": "📧 **PayPal:** dahn3854@gmail.com",
    "Revolut": "💳 **Revolut:** @dongnnb0b",
    "Apple Pay": "🔗 **Apple Pay:** https://revolut.me/dongnnb0b",
    "Debit/Credit Card": "🔗 **Debit/Credit Card:** https://revolut.me/dongnnb0b",
    "Bank Transfer": "👤 A staff member will provide bank transfer details shortly.",
    "PayPal Gift Card": "👤 A staff member will provide PayPal Gift Card details shortly.",
    "Crypto": "👤 A staff member will provide crypto details shortly.",
    "PaySafe Card": "👤 A staff member will provide PaySafe details shortly.",
}

SERVICE_ACTIVE_CHANNELS = {
    "ranked": "🟢｜active-ranked",
    "bulk-trophies": "🟢｜active-bulk-trophies",
    "prestige": "🟢｜active-prestige",
    "matcherino": "🟢｜active-matcherino",
    "championship": "🟢｜active-championship",
    "winstreaks": "🟢｜active-winstreaks",
    "tier-1": "🟢｜active-tier-1",
    "tier-2": "🟢｜active-tier-2",
    "tier-3": "🟢｜active-tier-3",
}

SERVICE_TITLES = {
    "ranked": ("🏅 Ranked Boost Order", "Your Ranked Boost Order"),
    "bulk-trophies": ("🏆 Trophy Boost Order", "Your Trophy Boost Order"),
    "prestige": ("⭐ Prestige Boost Order", "Your Prestige Boost Order"),
    "matcherino": ("🎯 Matcherino Boost Order", "Your Matcherino Boost Order"),
    "championship": ("🏆 Championship Boost Order", "Your Championship Boost Order"),
    "winstreaks": ("🔥 Winstreak Boost Order", "Your Winstreak Boost Order"),
    "tier-1": ("🥇 Tier 1 Account Order", "Your Tier 1 Account Order"),
    "tier-2": ("🥈 Tier 2 Account Order", "Your Tier 2 Account Order"),
    "tier-3": ("🥉 Tier 3 Account Order", "Your Tier 3 Account Order"),
}

IMAGES = {
    "ranked": "https://media.discordapp.net/attachments/1512925620169084968/1512959670476865676/image.png?ex=6a25fcfe&is=6a24ab7e&hm=cd95ede6d8e53bd66286ae88b27c7ff850a291308fcb653ed13e189472210812&=&format=webp&quality=lossless&width=2280&height=1272",
    "prestige": "https://media.discordapp.net/attachments/1512925620169084968/1512965912385421352/image.png?ex=6a2602cf&is=6a24b14f&hm=f45e7d5a1059d5ed59791c4417d4d1441614cd7b235f547a239393291175bc0d&=&format=webp&quality=lossless&width=2448&height=1272",
    "bulk-trophies": "https://media.discordapp.net/attachments/1512925620169084968/1512966361150787735/image.png?ex=6a26033a&is=6a24b1ba&hm=727d9d165fa4fdd10fa5653009e2914a9bf06f99b7b5c234710cc225c72d3f05&=&format=webp&quality=lossless&width=1100&height=616",
    "matcherino": "https://media.discordapp.net/attachments/1512925620169084968/1512966584631820490/image.png?ex=6a26036f&is=6a24b1ef&hm=a80906a8a34f53d2418f21b957e7d65d75151b8d18c6b532e5cf951b5652308a&=&format=webp&quality=lossless&width=2262&height=1272",
    "winstreaks": "https://media.discordapp.net/attachments/1512925620169084968/1512967580766175293/image.png?ex=6a26045c&is=6a24b2dc&hm=ee0854a41be7bf0d7314297e4ed9481de2d886daf4a7a8eea56bde763d87f3c4&=&format=webp&quality=lossless&width=1054&height=700",
    "championship": "https://media.discordapp.net/attachments/1512925620169084968/1512967994685526126/image.png?ex=6a2604bf&is=6a24b33f&hm=8c31044313dda43ca7848048e4e063756d3ea8385a65c69d3ea562770fe485dd&=&format=webp&quality=lossless&width=1100&height=438",
}

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def generate_ticket_number():
    return ''.join(random.choices(string.digits, k=4))

def get_payment_info(method):
    return PAYMENT_DETAILS.get(method, f"💳 **{method}** — A staff member will confirm details shortly.")

def stars(rating):
    return "⭐" * rating + "☆" * (5 - rating)

def build_confirm_embed(service_name, data):
    embed = discord.Embed(
        title=f"🎯 Confirm Your {service_name} Order",
        description="**Please review your order details and confirm:**",
        color=discord.Color.purple()
    )
    for key, value in data.items():
        if key == "Notes" and value == "None":
            continue
        embed.add_field(name=key, value=f"> {value}", inline=False)

    embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
    return embed

# ─────────────────────────────────────────────
# TICKET CORE
# ─────────────────────────────────────────────
async def create_ticket(guild, service, user, data):
    active_channel_name = SERVICE_ACTIVE_CHANNELS.get(service)
    active_channel = discord.utils.get(guild.channels, name=active_channel_name)
    if not active_channel: return None
    
    await active_channel.set_permissions(user, view_channel=True, send_messages=False, read_message_history=True)
    
    ticket_num = generate_ticket_number()
    thread = await active_channel.create_thread(name=f"{user.name}.{ticket_num}", type=discord.ChannelType.private_thread)
    
    await thread.add_user(user)
    try:
        owner_user = await guild.fetch_member(1070829490730705028) 
        if owner_user: await thread.add_user(owner_user)
    except: pass
    
    ticket_label, order_title = SERVICE_TITLES.get(service, ("📋 Order Ticket", "Your Order"))
    details_embed = discord.Embed(title=f"ℹ️ Order Details - {ticket_num}", description=f"**{order_title}**", color=discord.Color.purple())
    for k, v in data.items():
        if v != "None": details_embed.add_field(name=k, value=f"╰ {v}", inline=False)
    
    payment_method = data.get("Payment Method", "Unknown")
    details_embed.add_field(name="💳 Payment Details", value=get_payment_info(payment_method), inline=False)
    
    main_msg = await thread.send(embed=details_embed, view=CloseTicketView())
    
    async for message in thread.history(limit=50):
        if message.id != main_msg.id: await message.delete()
    
    owner = discord.utils.get(guild.roles, name="Owner")
    if owner: await thread.send(f"{owner.mention} New ticket opened!")
    
    return thread

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ticket closed.", ephemeral=True)
        if isinstance(interaction.channel, discord.Thread):
            await interaction.channel.edit(archived=True, locked=True)

    @discord.ui.button(label="Close With Reason", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket_reason")
    async def close_with_reason(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CloseReasonModal())

class CloseReasonModal(discord.ui.Modal, title="Close Ticket With Reason"):
    reason = discord.ui.TextInput(label="Reason", placeholder="Enter reason...", max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Closed: {self.reason.value}", ephemeral=True)
        if isinstance(interaction.channel, discord.Thread):
            await interaction.channel.edit(archived=True, locked=True)

class ConfirmOrderView(discord.ui.View):
    def __init__(self, service, data):
        super().__init__(timeout=None)
        self.service = service
        self.data = data

    @discord.ui.button(label="✅ Confirm & Create Ticket", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        try:
            thread = await create_ticket(interaction.guild, self.service, interaction.user, self.data)
            if thread:
                await interaction.edit_original_response(content=f"✅ Ticket created: {thread.mention}\nA staff member will confirm your price shortly.", embeds=[], view=None)
            else:
                await interaction.edit_original_response(content="❌ Could not find active channel.", embeds=[], view=None)
        except discord.errors.Forbidden:
            await interaction.edit_original_response(content="❌ **Permission Error:** Missing channel permissions.", embeds=[], view=None)
        except Exception as e:
            await interaction.edit_original_response(content=f"❌ **Error:** {e}", embeds=[], view=None)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Order cancelled.", embed=None, view=None)

# ─────────────────────────────────────────────
# TEXT-INPUT POP-UP MODALS (NO DROPDOWNS ALLOWED BY DISCORD)
# ─────────────────────────────────────────────
class RankedBoostModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title=f"Ranked Boost - {order_type}")
        self.order_type = order_type
        
        self.current_rank = discord.ui.TextInput(label="Current Rank", placeholder="e.g. Bronze 1", max_length=50)
        self.add_item(self.current_rank)
        self.desired_rank = discord.ui.TextInput(label="Desired Rank", placeholder="e.g. Mythic 1", max_length=50)
        self.add_item(self.desired_rank)
        self.power_11 = discord.ui.TextInput(label="Power 11 Brawlers", placeholder="e.g. 10", max_length=10)
        self.add_item(self.power_11)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="e.g. PayPal, Revolut", max_length=50)
        self.add_item(self.payment)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", style=discord.TextStyle.paragraph, required=False, max_length=500)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Current Rank": self.current_rank.value,
            "Desired Rank": self.desired_rank.value,
            "Power 11 Brawlers": self.power_11.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value or "None"
        }
        embed = build_confirm_embed("Ranked Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("ranked", data), ephemeral=True)

class TrophiesBoostModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title=f"Trophy Boost - {order_type}")
        self.order_type = order_type
        
        self.current_trophies = discord.ui.TextInput(label="Current Trophies", placeholder="e.g. 10k", max_length=50)
        self.add_item(self.current_trophies)
        self.desired_trophies = discord.ui.TextInput(label="Desired Trophies", placeholder="e.g. 20k", max_length=50)
        self.add_item(self.desired_trophies)
        self.power_11 = discord.ui.TextInput(label="Power 11 Brawlers", placeholder="e.g. 10", max_length=10)
        self.add_item(self.power_11)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="e.g. PayPal", max_length=50)
        self.add_item(self.payment)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", style=discord.TextStyle.paragraph, required=False, max_length=500)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Current Trophies": self.current_trophies.value,
            "Desired Trophies": self.desired_trophies.value,
            "Power 11 Brawlers": self.power_11.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value or "None"
        }
        embed = build_confirm_embed("Trophy Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("bulk-trophies", data), ephemeral=True)

class PrestigeBoostModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title=f"Prestige Boost - {order_type}")
        self.order_type = order_type
        
        self.brawler_name = discord.ui.TextInput(label="Brawler Name", placeholder="e.g. Shelly", max_length=50)
        self.add_item(self.brawler_name)
        self.current_prestige = discord.ui.TextInput(label="Current Prestige", placeholder="e.g. 0 Trophies", max_length=50)
        self.add_item(self.current_prestige)
        self.desired_prestige = discord.ui.TextInput(label="Desired Prestige", placeholder="e.g. Prestige 1", max_length=50)
        self.add_item(self.desired_prestige)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="e.g. PayPal", max_length=50)
        self.add_item(self.payment)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", style=discord.TextStyle.paragraph, required=False, max_length=500)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Brawler Name": self.brawler_name.value,
            "Current Prestige": self.current_prestige.value,
            "Desired Prestige": self.desired_prestige.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value or "None"
        }
        embed = build_confirm_embed("Prestige Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("prestige", data), ephemeral=True)

class WinstreakBoostModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title=f"Winstreak Order - {order_type}")
        self.order_type = order_type
        
        self.target_winstreak = discord.ui.TextInput(label="Target Winstreak", placeholder="e.g. 50 wins", max_length=50)
        self.add_item(self.target_winstreak)
        self.picker = discord.ui.TextInput(label="Who picks the brawler?", placeholder="Booster or Me", max_length=50)
        self.add_item(self.picker)
        self.power_11 = discord.ui.TextInput(label="Power 11 Brawlers", placeholder="e.g. 10", max_length=10)
        self.add_item(self.power_11)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="e.g. PayPal", max_length=50)
        self.add_item(self.payment)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", style=discord.TextStyle.paragraph, required=False, max_length=500)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Target Winstreak": self.target_winstreak.value,
            "Brawler Picker": self.picker.value,
            "Power 11 Brawlers": self.power_11.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value or "None"
        }
        embed = build_confirm_embed("Winstreak Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("winstreaks", data), ephemeral=True)

class MatcherinoBoostModal(discord.ui.Modal):
    def __init__(self, order_type, service_id, service_name):
        super().__init__(title=f"{service_name} - {order_type}")
        self.order_type = order_type
        self.service_id = service_id
        self.service_name = service_name
        
        self.brawler_count = discord.ui.TextInput(label="Brawler Count", placeholder="e.g. 60-70", max_length=50)
        self.add_item(self.brawler_count)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="e.g. PayPal", max_length=50)
        self.add_item(self.payment)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", style=discord.TextStyle.paragraph, required=False, max_length=500)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Brawler Count": self.brawler_count.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value or "None"
        }
        embed = build_confirm_embed(self.service_name, data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView(self.service_id, data), ephemeral=True)

class TierModal(discord.ui.Modal):
    def __init__(self, tier):
        super().__init__(title=f"Tier {tier} Account Order")
        self.tier = tier
        
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="e.g. PayPal", max_length=50)
        self.add_item(self.payment)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", style=discord.TextStyle.paragraph, required=False, max_length=500)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Account Tier": f"Tier {self.tier}",
            "Payment Method": self.payment.value,
            "Notes": self.notes.value or "None"
        }
        embed = build_confirm_embed(f"Tier {self.tier} Account", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView(f"tier-{self.tier}", data), ephemeral=True)

# ─────────────────────────────────────────────
# PERSISTENT BUTTON VIEWS
# ─────────────────────────────────────────────
async def safe_send_modal(interaction, modal):
    try:
        await interaction.response.send_modal(modal)
    except Exception as e:
        if not interaction.response.is_done():
            await interaction.response.send_message(f"❌ Failed to open form: {e}", ephemeral=True)
        else:
            await interaction.followup.send(f"❌ Failed to open form: {e}", ephemeral=True)

class RankedOrderView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="ranked_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose service type:", description="🚀 **B00st** - Standard\n🤝 **Carry** - Play together", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=RankedBoostCarryView(), ephemeral=True)

class RankedBoostCarryView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="r_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, RankedBoostModal("Boost"))
    @discord.ui.button(label="Get Carried", style=discord.ButtonStyle.primary, emoji="💎", custom_id="r_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, RankedBoostModal("Carry"))

class TrophiesOrderView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="trophies_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose service type:", description="🚀 **B00st** - Standard\n🤝 **Carry** - Play together", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=TrophiesBoostCarryView(), ephemeral=True)

class TrophiesBoostCarryView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="t_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, TrophiesBoostModal("Boost"))
    @discord.ui.button(label="Get Carried", style=discord.ButtonStyle.primary, emoji="💎", custom_id="t_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, TrophiesBoostModal("Carry"))

class PrestigeOrderView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="prestige_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose service type:", description="🚀 **B00st** - Standard\n🤝 **Carry** - Play together", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=PrestigeBoostCarryView(), ephemeral=True)

class PrestigeBoostCarryView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="p_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, PrestigeBoostModal("Boost"))
    @discord.ui.button(label="Get Carried", style=discord.ButtonStyle.primary, emoji="💎", custom_id="p_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, PrestigeBoostModal("Carry"))

class WinstreakOrderView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="ws_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose service type:", description="🚀 **B00st** - Standard\n🤝 **Carry** - Play together", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=WinstreakBoostCarryView(), ephemeral=True)

class WinstreakBoostCarryView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="w_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, WinstreakBoostModal("Boost"))
    @discord.ui.button(label="Get Carried", style=discord.ButtonStyle.primary, emoji="💎", custom_id="w_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, WinstreakBoostModal("Carry"))

class MatcherinoOrderView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="m_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose service type:", description="🚀 **B00st** - Standard\n🤝 **Carry** - Play together", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=MatchBoostCarryView("matcherino", "Matcherino Boost"), ephemeral=True)

class ChampionshipOrderView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="c_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose service type:", description="🚀 **B00st** - Standard\n🤝 **Carry** - Play together", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=MatchBoostCarryView("championship", "Championship Boost"), ephemeral=True)

class MatchBoostCarryView(discord.ui.View):
    def __init__(self, s, sn): super().__init__(timeout=None); self.s, self.sn = s, sn
    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, MatcherinoBoostModal("Boost", self.s, self.sn))
    @discord.ui.button(label="Get Carried", style=discord.ButtonStyle.primary, emoji="💎")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await safe_send_modal(interaction, MatcherinoBoostModal("Carry", self.s, self.sn))

class TierOrderView(discord.ui.View):
    def __init__(self, tier, service):
        super().__init__(timeout=None)
        self.tier = tier
        self.service = service
        btn = discord.ui.Button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id=f"tier_{tier}_order_now")
        btn.callback = self.order_now
        self.add_item(btn)

    async def order_now(self, interaction: discord.Interaction):
        await safe_send_modal(interaction, TierModal(self.tier))

# ─────────────────────────────────────────────
# MAIN MENU DROPDOWN & SUPPORT
# ─────────────────────────────────────────────
class ServiceSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Select a service...",
        custom_id="main_service_select",
        options=[
            discord.SelectOption(label="Boost / Carry Service", description="Trophy, Ranked, Prestige, Winstreak, Matcherino & more", emoji="📊"),
            discord.SelectOption(label="Other Queries", description="General questions, support & other requests", emoji="🎫"),
        ]
    )
    async def select_service(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values[0] == "Boost / Carry Service":
            guild = interaction.guild
            def ch(name):
                c = discord.utils.get(guild.channels, name=name)
                return c.mention if c else name

            embed = discord.Embed(title="📊 Boost & Carry Services", description="ℹ️ Click the channel that matches your desired service.", color=discord.Color.purple())
            embed.add_field(name="", value=(
                f"> **Trophy** — {ch('⚡｜bulk-trophies')}\n"
                f"> **Matcherino** — {ch('⚡｜matcherino')}\n"
                f"> **Ranked** — {ch('⚡｜ranked')}\n"
                f"> **Winstreak** — {ch('⚡｜winstreaks')}\n"
                f"> **Prestige** — {ch('⚡｜prestige')}\n"
                f"> **Championship** — {ch('⚡｜championship-challenge')}"
            ), inline=False)
            embed.set_footer(text=f"Powered by {BRAND}")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            guild = interaction.guild
            others_channel = discord.utils.get(guild.channels, name="🟢｜active-support")
            if others_channel:
                thread = await others_channel.create_thread(name=f"Support — {interaction.user.name}", type=discord.ChannelType.private_thread)
                embed = discord.Embed(title="🎫 Support Ticket Opened", description=f"Welcome {interaction.user.mention}! A staff member will be with you shortly.", color=discord.Color.blue())
                embed.set_footer(text=f"Powered by {BRAND}")
                await thread.send(embed=embed, view=CloseTicketView())
                await thread.add_user(interaction.user)

                owner_role = discord.utils.get(guild.roles, name="Owner")
                if owner_role: await thread.send(f"{owner_role.mention} New support ticket!")

                await interaction.response.send_message(f"✅ Support ticket created: {thread.mention}", ephemeral=True)
            else:
                await interaction.response.send_message("Support channel not found.", ephemeral=True)

# ─────────────────────────────────────────────
# REVIEW SYSTEM
# ─────────────────────────────────────────────
class ReviewRatingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for i in range(1, 6):
            btn = discord.ui.Button(label=f"{'⭐' * i}", style=discord.ButtonStyle.secondary, custom_id=f"review_star_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)

    def make_callback(self, rating):
        async def callback(interaction: discord.Interaction):
            await safe_send_modal(interaction, ReviewCommentModal(rating))
        return callback

class ReviewCommentModal(discord.ui.Modal):
    def __init__(self, rating):
        super().__init__(title=f"Review — {rating}/5 Stars")
        self.rating = rating
        self.comment = discord.ui.TextInput(label="Comment", placeholder="Tell us about your experience...", max_length=500, required=False)
        self.add_item(self.comment)

    async def on_submit(self, interaction: discord.Interaction):
        view = ReviewPostView(self.rating, self.comment.value or "No comment")
        await interaction.response.send_message("How would you like to post your review?", view=view, ephemeral=True)

class ReviewPostView(discord.ui.View):
    def __init__(self, rating, comment):
        super().__init__(timeout=None)
        self.rating, self.comment = rating, comment

    @discord.ui.button(label="Post with Username", style=discord.ButtonStyle.primary, custom_id="review_post_username")
    async def post_with_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.post_review(interaction, anonymous=False)

    @discord.ui.button(label="Post Anonymously", style=discord.ButtonStyle.secondary, custom_id="review_post_anon")
    async def post_anon(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.post_review(interaction, anonymous=True)

    async def post_review(self, interaction: discord.Interaction, anonymous: bool):
        guild = interaction.guild or (bot.guilds[0] if bot.guilds else None)
        if not guild: return await interaction.response.send_message("Could not find server.", ephemeral=True)

        reviews_channel = discord.utils.get(guild.channels, name="✏️｜clients-opinion")
        if not reviews_channel: return await interaction.response.send_message("Reviews channel not found.", ephemeral=True)

        display_name = "Anonymous" if anonymous else interaction.user.name
        embed = discord.Embed(title=f"⭐ New Review from {display_name}", color=discord.Color.gold())
        embed.add_field(name=f"⭐ Rating ({self.rating}/5)", value=f"> {stars(self.rating)}", inline=False)
        embed.add_field(name="ℹ️ Comment", value=f"> {self.comment}", inline=False)
        if not anonymous: embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"Powered by {BRAND} | {discord.utils.utcnow().strftime('%A, %d %B %Y at %H:%M')}")

        await reviews_channel.send(embed=embed)
        await interaction.response.edit_message(content="✅ Review posted! Thank you!", view=None)

# ─────────────────────────────────────────────
# SLASH COMMANDS FOR SETUP
# ─────────────────────────────────────────────
async def safe_send_panel(interaction, embed, view, success_msg):
    await interaction.response.defer(ephemeral=True)
    try:
        if embed: await interaction.channel.send(embed=embed, view=view)
        else: await interaction.channel.send(view=view)
        await interaction.followup.send(success_msg)
    except discord.errors.Forbidden:
        await interaction.followup.send("❌ **Error:** I don't have permission to send messages or embed links.")
    except Exception as e:
        await interaction.followup.send(f"❌ **Error:** {e}")

@bot.tree.command(name="setup-order-here", description="Post the main order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_order_here(interaction: discord.Interaction):
    embed = discord.Embed(title="Select An Option Below ✏️", color=discord.Color.purple())
    embed.add_field(name="📋 Rules", value="• Follow directions of FastBrawl™ Bot\n• Do not spam ping staff\n• Be patient", inline=False)
    embed.set_footer(text=f"Powered by {BRAND}")
    await safe_send_panel(interaction, embed, ServiceSelectView(), "✅ Order panel posted!")

@bot.tree.command(name="setup-ranked", description="Post the ranked order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_ranked(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Ranked B00st Service", description="**What We Offer**\n• Climb the ranks securely", color=discord.Color.blue())
    embed.set_image(url=IMAGES["ranked"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await safe_send_panel(interaction, embed, RankedOrderView(), "✅ Ranked panel posted!")

@bot.tree.command(name="setup-trophies", description="Post the trophies order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_trophies(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Trophy B00st Service", description="**What We Offer**\n• Safe and efficient trophy farming", color=discord.Color.gold())
    embed.set_image(url=IMAGES["bulk-trophies"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await safe_send_panel(interaction, embed, TrophiesOrderView(), "✅ Trophies panel posted!")

@bot.tree.command(name="setup-prestige", description="Post the prestige order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_prestige(interaction: discord.Interaction):
    embed = discord.Embed(title="⭐ Prestige B00st Service", description="**What We Offer**\n• Quick prestige progression", color=discord.Color.purple())
    embed.set_image(url=IMAGES["prestige"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await safe_send_panel(interaction, embed, PrestigeOrderView(), "✅ Prestige panel posted!")

@bot.tree.command(name="setup-winstreak", description="Post the winstreak order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_winstreak(interaction: discord.Interaction):
    embed = discord.Embed(title="🔥 Winstreak B00st Service", description="**What We Offer**\n• Dominate matches with pro players", color=discord.Color.orange())
    embed.set_image(url=IMAGES["winstreaks"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await safe_send_panel(interaction, embed, WinstreakOrderView(), "✅ Winstreak panel posted!")

@bot.tree.command(name="setup-matcherino", description="Post the matcherino order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_matcherino(interaction: discord.Interaction):
    embed = discord.Embed(title="🎯 Matcherino B00st Service", description="**What We Offer**\n• Professional tournament services", color=discord.Color.green())
    embed.set_image(url=IMAGES["matcherino"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await safe_send_panel(interaction, embed, MatcherinoOrderView(), "✅ Matcherino panel posted!")

@bot.tree.command(name="setup-championship", description="Post the championship order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_championship(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Championship B00st Service", description="**What We Offer**\n• Fast challenge wins", color=discord.Color.yellow())
    embed.set_image(url=IMAGES["championship"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await safe_send_panel(interaction, embed, ChampionshipOrderView(), "✅ Championship panel posted!")

@bot.tree.command(name="setup-tier1", description="Post the Tier 1 order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tier1(interaction: discord.Interaction):
    await safe_send_panel(interaction, None, TierOrderView("1", "tier-1"), "✅ Tier 1 panel posted!")

@bot.tree.command(name="setup-tier2", description="Post the Tier 2 order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tier2(interaction: discord.Interaction):
    await safe_send_panel(interaction, None, TierOrderView("2", "tier-2"), "✅ Tier 2 panel posted!")

@bot.tree.command(name="setup-tier3", description="Post the Tier 3 order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tier3(interaction: discord.Interaction):
    await safe_send_panel(interaction, None, TierOrderView("3", "tier-3"), "✅ Tier 3 panel posted!")

@bot.tree.command(name="review", description="Send a review request to a user")
@app_commands.checks.has_permissions(administrator=True)
async def review(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=True)
    try:
        embed = discord.Embed(title="⭐ Leave a Review", description="How was your experience?\nSelect a rating below!", color=discord.Color.gold())
        embed.set_footer(text=f"Powered by {BRAND}")
        await user.send(embed=embed, view=ReviewRatingView())
        await interaction.followup.send(f"✅ Review request sent to {user.mention}!")
    except:
        await interaction.followup.send(f"❌ Could not DM {user.mention}.")

# ─────────────────────────────────────────────
# BOT EVENTS
# ─────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    
    bot.add_view(ServiceSelectView())
    bot.add_view(CloseTicketView())
    bot.add_view(RankedOrderView())
    bot.add_view(RankedBoostCarryView())
    bot.add_view(TrophiesOrderView())
    bot.add_view(TrophiesBoostCarryView())
    bot.add_view(PrestigeOrderView())
    bot.add_view(PrestigeBoostCarryView())
    bot.add_view(WinstreakOrderView())
    bot.add_view(WinstreakBoostCarryView())
    bot.add_view(MatcherinoOrderView())
    bot.add_view(ChampionshipOrderView())

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync: {e}")

if not TOKEN:
    print("❌ TOKEN not found.")
    exit()

bot.run(TOKEN)
