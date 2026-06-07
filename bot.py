import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random
import string

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
    "prestige": "https://media.discordapp.net/attachments/1512925620169084968/1513282537710161960/Screenshot_2026-06-07_at_21.44.21.png?ex=6a2729b0&is=6a25d830&hm=2294cd17c2328394617034f0a22f4d458f1cee8875de5f1b7edc27f3a2e095de&=&format=webp&quality=lossless&width=2394&height=1272",
    "bulk-trophies": "https://media.discordapp.net/attachments/1512925620169084968/1512966361150787735/image.png?ex=6a26033a&is=6a24b1ba&hm=727d9d165fa4fdd10fa5653009e2914a9bf06f99b7b5c234710cc225c72d3f05&=&format=webp&quality=lossless&width=1100&height=616",
    "matcherino": "https://media.discordapp.net/attachments/1512925620169084968/1512966584631820490/image.png?ex=6a26036f&is=6a24b1ef&hm=a80906a8a34f53d2418f21b957e7d65d75151b8d18c6b532e5cf951b5652308a&=&format=webp&quality=lossless&width=2262&height=1272",
    "winstreaks": "https://media.discordapp.net/attachments/1512925620169084968/1512967580766175293/image.png?ex=6a26045c&is=6a24b2dc&hm=ee0854a41be7bf0d7314297e4ed9481de2d886daf4a7a8eea56bde763d87f3c4&=&format=webp&quality=lossless&width=1054&height=700",
    "championship": "https://media.discordapp.net/attachments/1512925620169084968/1512967994685526126/image.png?ex=6a2604bf&is=6a24b33f&hm=8c31044313dda43ca7848048e4e063756d3ea8385a65c69d3ea562770fe485dd&=&format=webp&quality=lossless&width=1100&height=438",
}

def generate_ticket_number():
    return ''.join(random.choices(string.digits, k=4))

def get_payment_info(method):
    return PAYMENT_DETAILS.get(method, f"💳 **{method}** — A staff member will confirm details shortly.")

def stars(rating):
    return "⭐" * rating + "☆" * (5 - rating)

# ─────────────────────────────────────────────
# CREATE TICKET
# ─────────────────────────────────────────────
async def create_ticket(guild, service, user, data):
    active_channel_name = SERVICE_ACTIVE_CHANNELS.get(service, "active-ranked")
    active_channel = discord.utils.get(guild.channels, name=active_channel_name)
    if not active_channel:
        return None

    ticket_num = generate_ticket_number()
    thread = await active_channel.create_thread(
        name=f"{user.name}.{ticket_num}",
        type=discord.ChannelType.public_thread,
        auto_archive_duration=10080
    )

    # Delete the "started a thread" message
    await discord.utils.sleep_until(discord.utils.utcnow())
    async for message in active_channel.history(limit=5):
        if message.type == discord.MessageType.thread_created:
            await message.delete()
            break

    ticket_label, order_title = SERVICE_TITLES.get(service, ("📋 Order Ticket", "Your Order"))

    header_embed = discord.Embed(
        title=f"{ticket_label} is now open! 🎮",
        description="**Click the button below to close this ticket when you're done.**",
        color=discord.Color.green()
    )
    header_embed.set_footer(text=f"Powered by {BRAND}")

    details_embed = discord.Embed(
        title="ℹ️ Order Details",
        description=f"**{order_title}**",
        color=discord.Color.purple()
    )
    for key, value in data.items():
        if key == "Notes" and (value == "None" or not value):
            continue
        details_embed.add_field(name=key, value=f"╰ {value}", inline=False)
    details_embed.add_field(name="Customer", value=f"╰ {user.mention}", inline=False)
    payment_method = data.get("Payment Method", "")
    details_embed.add_field(name="💳 Payment Details", value=get_payment_info(payment_method), inline=False)
    details_embed.set_footer(text=f"Powered by {BRAND} • Ticket #{ticket_num}")

    await thread.send(embeds=[header_embed, details_embed], view=CloseTicketView())
    await thread.add_user(user)

    owner_role = discord.utils.get(guild.roles, name="Owner")
    if owner_role:
        await thread.send(f"{owner_role.mention} New ticket opened!", delete_after=5)

    return thread

# ─────────────────────────────────────────────
# CLOSE TICKET
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# CONFIRM VIEW
# ─────────────────────────────────────────────
class ConfirmOrderView(discord.ui.View):
    def __init__(self, service, data):
        super().__init__(timeout=None)
        self.service = service
        self.data = data

    @discord.ui.button(label="✅ Confirm & Create Ticket", style=discord.ButtonStyle.success, custom_id="confirm_order_btn")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        thread = await create_ticket(interaction.guild, self.service, interaction.user, self.data)
        if thread:
            await interaction.response.edit_message(content=f"✅ Ticket created: {thread.mention}\nA staff member will confirm your price shortly.", embed=None, view=None)
        else:
            await interaction.response.edit_message(content="❌ Could not find active channel. Contact an admin.", embed=None, view=None)

    @discord.ui.button(label="🔄 Change Selections", style=discord.ButtonStyle.secondary, custom_id="change_order_btn")
    async def change(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Please click Order Now again to restart.", embed=None, view=None)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger, custom_id="cancel_order_btn")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Order cancelled.", embed=None, view=None)

def build_confirm_embed(service_name, data):
    embed = discord.Embed(
        title=f"🎯 Confirm Your {service_name} Order",
        description="**Please review your order details and confirm:**",
        color=discord.Color.purple()
    )
    for key, value in data.items():
        if key == "Notes" and (value == "None" or not value):
            continue
        embed.add_field(name=key, value=f"> {value}", inline=False)
    embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
    return embed

# ─────────────────────────────────────────────
# BOOST/CARRY VIEW
# ─────────────────────────────────────────────
def make_boost_carry_view(boost_custom_id, carry_custom_id, boost_callback, carry_callback):
    class BoostCarryView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
    btn_boost = discord.ui.Button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id=boost_custom_id)
    btn_boost.callback = boost_callback
    btn_carry = discord.ui.Button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id=carry_custom_id)
    btn_carry.callback = carry_callback
    view = BoostCarryView()
    view.add_item(btn_boost)
    view.add_item(btn_carry)
    return view

# ─────────────────────────────────────────────
# RANKED
# ─────────────────────────────────────────────
class RankedFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title=f"Ranked {'Boost' if order_type == 'Boost' else 'Carry'} Order")
        self.order_type = order_type
        self.current_rank = discord.ui.TextInput(label="Current Rank", placeholder="e.g. Bronze I, Silver II, Gold III, Diamond I...", max_length=20)
        self.desired_rank = discord.ui.TextInput(label="Desired Rank (min Diamond I)", placeholder="e.g. Diamond I, Mythic II, Masters I, Pro...", max_length=20)
        self.power11 = discord.ui.TextInput(label="How many Power 11 brawlers do you have?", placeholder="e.g. 0-10, 11-20, 51-60, 100+", max_length=10)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="PayPal / Revolut / Apple Pay / Bank Transfer / etc.", max_length=50)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", placeholder="Any special requests...", required=False, max_length=500, style=discord.TextStyle.paragraph)
        self.add_item(self.current_rank)
        self.add_item(self.desired_rank)
        self.add_item(self.power11)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Current Rank": self.current_rank.value,
            "Desired Rank": self.desired_rank.value,
            "Power 11 Brawlers": self.power11.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None",
        }
        embed = build_confirm_embed("Ranked Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("ranked", data), ephemeral=True)

class RankedOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="ranked_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=RankedBoostCarryView(), ephemeral=True)

class RankedBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="ranked_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RankedFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="ranked_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RankedFormModal("Carry"))

# ─────────────────────────────────────────────
# TROPHIES
# ─────────────────────────────────────────────
class TrophiesFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title="Trophy Boost Order")
        self.order_type = order_type
        self.current_range = discord.ui.TextInput(label="Current Trophy Range", placeholder="e.g. 0-10k, 20-30k, 50-60k, 100-125k...", max_length=20)
        self.desired_range = discord.ui.TextInput(label="Desired Trophy Range", placeholder="e.g. 10-20k, 50-60k, 125-150k...", max_length=20)
        self.power11 = discord.ui.TextInput(label="How many Power 11 brawlers do you have?", placeholder="e.g. 0-10, 11-20, 51-60, 100+", max_length=10)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="PayPal / Revolut / Apple Pay / Bank Transfer / etc.", max_length=50)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", placeholder="Any special requests...", required=False, max_length=500, style=discord.TextStyle.paragraph)
        self.add_item(self.current_range)
        self.add_item(self.desired_range)
        self.add_item(self.power11)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Current Trophy Range": self.current_range.value,
            "Desired Trophy Range": self.desired_range.value,
            "Power 11 Brawlers": self.power11.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None",
        }
        embed = build_confirm_embed("Trophy Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("bulk-trophies", data), ephemeral=True)

class TrophiesOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="trophies_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=TrophiesBoostCarryView(), ephemeral=True)

class TrophiesBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="trophies_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TrophiesFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="trophies_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TrophiesFormModal("Carry"))

# ─────────────────────────────────────────────
# PRESTIGE
# ─────────────────────────────────────────────
class PrestigeFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title="Prestige Boost Order")
        self.order_type = order_type
        self.brawler = discord.ui.TextInput(label="Brawler Name", placeholder="Enter the brawler name...", max_length=30)
        self.current_prestige = discord.ui.TextInput(label="Current Prestige", placeholder="0 Trophies / Prestige 1 / Prestige 2 / Prestige 3", max_length=20)
        self.desired_prestige = discord.ui.TextInput(label="Desired Prestige", placeholder="Prestige 1 / Prestige 2 / Prestige 3", max_length=20)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="PayPal / Revolut / Apple Pay / Bank Transfer / etc.", max_length=50)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", placeholder="Any special requests...", required=False, max_length=300, style=discord.TextStyle.paragraph)
        self.add_item(self.brawler)
        self.add_item(self.current_prestige)
        self.add_item(self.desired_prestige)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Brawler": self.brawler.value,
            "Current Prestige": self.current_prestige.value,
            "Desired Prestige": self.desired_prestige.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None",
        }
        embed = build_confirm_embed("Prestige Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("prestige", data), ephemeral=True)

class PrestigeOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="prestige_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=PrestigeBoostCarryView(), ephemeral=True)

class PrestigeBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="prestige_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PrestigeFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="prestige_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PrestigeFormModal("Carry"))

# ─────────────────────────────────────────────
# WINSTREAK
# ─────────────────────────────────────────────
class WinstreakFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title="Winstreak Boost Order")
        self.order_type = order_type
        self.target = discord.ui.TextInput(label="Target Winstreak", placeholder="50 wins / 67 wins / 69 wins / 101 wins / 111 wins / 125 wins / 200 wins", max_length=20)
        self.picker = discord.ui.TextInput(label="Who chooses the brawler?", placeholder="Booster chooses (Normal Price) / I choose the brawler (+€5)", max_length=40)
        self.power11 = discord.ui.TextInput(label="How many Power 11 brawlers do you have?", placeholder="e.g. 0-10, 11-20, 51-60, 100+", max_length=10)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="PayPal / Revolut / Apple Pay / Bank Transfer / etc.", max_length=50)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", placeholder="Any special requests...", required=False, max_length=300, style=discord.TextStyle.paragraph)
        self.add_item(self.target)
        self.add_item(self.picker)
        self.add_item(self.power11)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Target Winstreak": self.target.value,
            "Brawler Picker": self.picker.value,
            "Power 11 Brawlers": self.power11.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None",
        }
        embed = build_confirm_embed("Winstreak Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("winstreaks", data), ephemeral=True)

class WinstreakOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="winstreak_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=WinstreakBoostCarryView(), ephemeral=True)

class WinstreakBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="winstreak_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WinstreakFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="winstreak_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WinstreakFormModal("Carry"))

# ─────────────────────────────────────────────
# MATCHERINO
# ─────────────────────────────────────────────
class MatcherinoFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title="Matcherino Boost Order")
        self.order_type = order_type
        self.brawlers = discord.ui.TextInput(label="How many brawlers do you have?", placeholder="60-70 Brawlers / 70-80 Brawlers / 80-90 Brawlers / 90+ Brawlers", max_length=20)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="PayPal / Revolut / Apple Pay / Bank Transfer / etc.", max_length=50)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", placeholder="Any special requests...", required=False, max_length=500, style=discord.TextStyle.paragraph)
        self.add_item(self.brawlers)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Brawler Count": self.brawlers.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None",
        }
        embed = build_confirm_embed("Matcherino Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("matcherino", data), ephemeral=True)

class MatcherinoOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="matcherino_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=MatcherinoBoostCarryView(), ephemeral=True)

class MatcherinoBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="matcherino_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MatcherinoFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="matcherino_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MatcherinoFormModal("Carry"))

# ─────────────────────────────────────────────
# CHAMPIONSHIP
# ─────────────────────────────────────────────
class ChampionshipFormModal(discord.ui.Modal):
    def __init__(self, order_type):
        super().__init__(title="Championship Boost Order")
        self.order_type = order_type
        self.brawlers = discord.ui.TextInput(label="How many brawlers do you have?", placeholder="60-70 Brawlers / 70-80 Brawlers / 80-90 Brawlers / 90+ Brawlers", max_length=20)
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="PayPal / Revolut / Apple Pay / Bank Transfer / etc.", max_length=50)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", placeholder="Any special requests...", required=False, max_length=500, style=discord.TextStyle.paragraph)
        self.add_item(self.brawlers)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Order Type": self.order_type,
            "Brawler Count": self.brawlers.value,
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None",
        }
        embed = build_confirm_embed("Championship Boost", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView("championship", data), ephemeral=True)

class ChampionshipOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="championship_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=ChampionshipBoostCarryView(), ephemeral=True)

class ChampionshipBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="championship_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ChampionshipFormModal("Boost"))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="championship_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ChampionshipFormModal("Carry"))

# ─────────────────────────────────────────────
# TIER
# ─────────────────────────────────────────────
class TierFormModal(discord.ui.Modal):
    def __init__(self, tier, service):
        super().__init__(title=f"Tier {tier} Account Order")
        self.tier = tier
        self.service = service
        self.payment = discord.ui.TextInput(label="Payment Method", placeholder="PayPal / Revolut / Apple Pay / Bank Transfer / etc.", max_length=50)
        self.notes = discord.ui.TextInput(label="Additional Notes (Optional)", placeholder="Any special requests...", required=False, max_length=500, style=discord.TextStyle.paragraph)
        self.add_item(self.payment)
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction):
        data = {
            "Account Tier": f"Tier {self.tier}",
            "Payment Method": self.payment.value,
            "Notes": self.notes.value if self.notes.value else "None",
        }
        embed = build_confirm_embed(f"Tier {self.tier} Account", data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView(self.service, data), ephemeral=True)

class TierOrderView(discord.ui.View):
    def __init__(self, tier, service):
        super().__init__(timeout=None)
        self.tier = tier
        self.service = service
        btn = discord.ui.Button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id=f"tier_{tier}_order_now")
        btn.callback = self.order_now
        self.add_item(btn)

    async def order_now(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TierFormModal(self.tier, self.service))

# ─────────────────────────────────────────────
# ORDER-HERE
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
        value = select.values[0]
        if value == "Boost / Carry Service":
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
                thread = await others_channel.create_thread(name=f"Support — {interaction.user.name}", type=discord.ChannelType.public_thread, auto_archive_duration=10080)
                embed = discord.Embed(title="🎫 Support Ticket Opened", description=f"Welcome {interaction.user.mention}! A staff member will be with you shortly.", color=discord.Color.blue())
                embed.set_footer(text=f"Powered by {BRAND}")
                await thread.send(embed=embed, view=CloseTicketView())
                await thread.add_user(interaction.user)
                owner_role = discord.utils.get(guild.roles, name="Owner")
                if owner_role:
                    await thread.send(f"{owner_role.mention} New support ticket!", delete_after=5)
                await interaction.response.send_message(f"✅ Support ticket created: {thread.mention}", ephemeral=True)
            else:
                await interaction.response.send_message("Support channel not found. Contact an admin.", ephemeral=True)

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
            await interaction.response.send_modal(ReviewCommentModal(rating))
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
        self.rating = rating
        self.comment = comment

    @discord.ui.button(label="Post with Username", style=discord.ButtonStyle.primary, custom_id="review_post_username")
    async def post_with_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.post_review(interaction, anonymous=False)

    @discord.ui.button(label="Post Anonymously", style=discord.ButtonStyle.secondary, custom_id="review_post_anon")
    async def post_anon(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.post_review(interaction, anonymous=True)

    async def post_review(self, interaction: discord.Interaction, anonymous: bool):
        guild = interaction.guild or (bot.guilds[0] if bot.guilds else None)
        if not guild:
            await interaction.response.send_message("Could not find server.", ephemeral=True)
            return
        reviews_channel = discord.utils.get(guild.channels, name="✏️｜clients-opinion")
        if not reviews_channel:
            await interaction.response.send_message("Reviews channel not found.", ephemeral=True)
            return
        display_name = "Anonymous" if anonymous else interaction.user.name
        embed = discord.Embed(title=f"⭐ New Review from {display_name}", color=discord.Color.gold())
        embed.add_field(name=f"⭐ Rating ({self.rating}/5)", value=f"> {stars(self.rating)}", inline=False)
        embed.add_field(name="ℹ️ Comment", value=f"> {self.comment}", inline=False)
        if not anonymous:
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"Powered by {BRAND} | {discord.utils.utcnow().strftime('%A, %d %B %Y at %H:%M')}")
        await reviews_channel.send(embed=embed)
        await interaction.response.edit_message(content="✅ Review posted! Thank you!", view=None)

# ─────────────────────────────────────────────
# SLASH COMMANDS
# ─────────────────────────────────────────────
@bot.tree.command(name="setup-order-here", description="Post the main order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_order_here(interaction: discord.Interaction):
    embed = discord.Embed(title="Select An Option Below ✏️", color=discord.Color.purple())
    embed.add_field(name="📋 Rules", value="• Follow the directions of FastBrawl™ Bot if given\n• Do not spam ping staff\n• Be patient, support has many tickets to handle", inline=False)
    embed.add_field(name="", value="**Select what type of ticket you want to be opened from the dropdown below ↓**", inline=False)
    embed.set_footer(text=f"Powered by {BRAND}")
    await interaction.channel.send(embed=embed, view=ServiceSelectView())
    await interaction.response.send_message("✅ Order panel posted!", ephemeral=True)

@bot.tree.command(name="setup-ranked", description="Post the ranked order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_ranked(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Ranked B00st Service", description="**What We Offer**\n• Climb the ranks with professional boosting service\n• Fast, secure, and reliable rank progression\n• Experienced boosters with proven track records", color=discord.Color.blue())
    embed.set_image(url=IMAGES["ranked"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await interaction.channel.send(embed=embed, view=RankedOrderView())
    await interaction.response.send_message("✅ Ranked panel posted!", ephemeral=True)

@bot.tree.command(name="setup-trophies", description="Post the trophies order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_trophies(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Trophy B00st Service", description="**What We Offer**\n• Boost your trophy count to reach new milestones\n• Safe and efficient trophy farming service\n• Achieve your trophy goals with expert help", color=discord.Color.gold())
    embed.set_image(url=IMAGES["bulk-trophies"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await interaction.channel.send(embed=embed, view=TrophiesOrderView())
    await interaction.response.send_message("✅ Trophies panel posted!", ephemeral=True)

@bot.tree.command(name="setup-prestige", description="Post the prestige order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_prestige(interaction: discord.Interaction):
    embed = discord.Embed(title="⭐ Prestige B00st Service", description="**What We Offer**\n• Unlock prestige levels for your brawlers\n• Quick and efficient prestige progression\n• Show off your dedication with prestige ranks", color=discord.Color.purple())
    embed.set_image(url=IMAGES["prestige"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await interaction.channel.send(embed=embed, view=PrestigeOrderView())
    await interaction.response.send_message("✅ Prestige panel posted!", ephemeral=True)

@bot.tree.command(name="setup-winstreak", description="Post the winstreak order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_winstreak(interaction: discord.Interaction):
    embed = discord.Embed(title="🔥 Winstreak B00st Service", description="**What We Offer**\n• Achieve impressive winstreaks with pro players\n• Dominate matches and build your streak\n• Consistent wins with skilled teammates", color=discord.Color.orange())
    embed.set_image(url=IMAGES["winstreaks"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await interaction.channel.send(embed=embed, view=WinstreakOrderView())
    await interaction.response.send_message("✅ Winstreak panel posted!", ephemeral=True)

@bot.tree.command(name="setup-matcherino", description="Post the matcherino order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_matcherino(interaction: discord.Interaction):
    embed = discord.Embed(title="🎯 Matcherino B00st Service", description="**What We Offer**\n• Professional matcherino tournament services\n• Competitive edge with experienced players\n• Tournament ready team support", color=discord.Color.green())
    embed.set_image(url=IMAGES["matcherino"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await interaction.channel.send(embed=embed, view=MatcherinoOrderView())
    await interaction.response.send_message("✅ Matcherino panel posted!", ephemeral=True)

@bot.tree.command(name="setup-championship", description="Post the championship order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_championship(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Championship B00st Service", description="**What We Offer**\n• Professional and fast challenge wins\n• Chance for you to compete in the Monthly Qualifiers\n• Competitive and sharp profile", color=discord.Color.yellow())
    embed.set_image(url=IMAGES["championship"])
    embed.set_footer(text=f"Powered by {BRAND}")
    await interaction.channel.send(embed=embed, view=ChampionshipOrderView())
    await interaction.response.send_message("✅ Championship panel posted!", ephemeral=True)

@bot.tree.command(name="setup-tier1", description="Post the Tier 1 order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tier1(interaction: discord.Interaction):
    await interaction.channel.send(view=TierOrderView("1", "tier-1"))
    await interaction.response.send_message("✅ Tier 1 panel posted!", ephemeral=True)

@bot.tree.command(name="setup-tier2", description="Post the Tier 2 order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tier2(interaction: discord.Interaction):
    await interaction.channel.send(view=TierOrderView("2", "tier-2"))
    await interaction.response.send_message("✅ Tier 2 panel posted!", ephemeral=True)

@bot.tree.command(name="setup-tier3", description="Post the Tier 3 order panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tier3(interaction: discord.Interaction):
    await interaction.channel.send(view=TierOrderView("3", "tier-3"))
    await interaction.response.send_message("✅ Tier 3 panel posted!", ephemeral=True)

@bot.tree.command(name="review", description="Send a review request to a user")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(user="The user to send a review request to")
async def review(interaction: discord.Interaction, user: discord.Member):
    try:
        embed = discord.Embed(title="⭐ Leave a Review", description="How was your experience with Fast Brawl Services?\nSelect a star rating below!", color=discord.Color.gold())
        embed.set_footer(text=f"Powered by {BRAND}")
        await user.send(embed=embed, view=ReviewRatingView())
        await interaction.response.send_message(f"✅ Review request sent to {user.mention}!", ephemeral=True)
    except:
        await interaction.response.send_message(f"❌ Could not DM {user.mention}. They may have DMs disabled.", ephemeral=True)

# ─────────────────────────────────────────────
# BOT EVENTS
# ─────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    bot.add_view(ServiceSelectView())
    bot.add_view(RankedOrderView())
    bot.add_view(RankedBoostCarryView())
    bot.add_view(TrophiesOrderView())
    bot.add_view(TrophiesBoostCarryView())
    bot.add_view(PrestigeOrderView())
    bot.add_view(PrestigeBoostCarryView())
    bot.add_view(WinstreakOrderView())
    bot.add_view(WinstreakBoostCarryView())
    bot.add_view(MatcherinoOrderView())
    bot.add_view(MatcherinoBoostCarryView())
    bot.add_view(ChampionshipOrderView())
    bot.add_view(ChampionshipBoostCarryView())
    bot.add_view(CloseTicketView())
    bot.add_view(ConfirmOrderView("ranked", {}))
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync: {e}")

if not TOKEN:
    print("❌ TOKEN not found.")
    exit()

bot.run(TOKEN)
